import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import itertools
import uuid
import math

def fit_black_box(X, y, model=None, random_state=42):
    if model is None:
        model = RandomForestClassifier(n_estimators=200, random_state=random_state)
    model.fit(X, y)
    return model

def train_global_surrogate(black_box, X, max_depth=4, random_state=42):
    preds = black_box.predict(X)
    surrogate = DecisionTreeClassifier(max_depth=max_depth, random_state=random_state)
    surrogate.fit(X, preds)
    return surrogate

def local_surrogate_explanation(black_box, instance: pd.Series, X_background: pd.DataFrame, n_samples=500, kernel_width=None):
    Xb = X_background.reset_index(drop=True)
    m = len(instance)
    if kernel_width is None:
        kernel_width = np.sqrt(m) * 0.75
    samples_idx = np.random.randint(0, len(Xb), size=n_samples)
    perturbed = Xb.loc[samples_idx].copy().reset_index(drop=True)
    mask = np.random.binomial(1, 0.5, size=(n_samples, m))
    for i, col in enumerate(Xb.columns):
        perturbed.loc[mask[:, i] == 1, col] = instance[col]
    distances = np.linalg.norm((perturbed.values - instance.values).astype(float), axis=1)
    weights = np.exp(-(distances ** 2) / (2 * (kernel_width ** 2)))
    probs = black_box.predict_proba(perturbed) if hasattr(black_box, "predict_proba") else None
    y = black_box.predict(perturbed) if probs is None else probs[:, 1]
    Xmat = (perturbed - perturbed.mean()).astype(float).values
    reg = Ridge(alpha=1.0)
    reg.fit(Xmat, y, sample_weight=weights)
    coef = dict(zip(Xb.columns.tolist(), reg.coef_.tolist()))
    return {"coefficients": coef, "intercept": float(reg.intercept_), "weights": weights}

def shap_monte_carlo(black_box, instance: pd.Series, X_background: pd.DataFrame, nsamples=200):
    features = X_background.columns.tolist()
    m = len(features)
    phi = dict((f, 0.0) for f in features)
    baseline = black_box.predict_proba(X_background).mean(axis=0) if hasattr(black_box, "predict_proba") else None
    for _ in range(nsamples):
        perm = np.random.permutation(m)
        current = X_background.mean().copy()
        prev_pred = black_box.predict_proba(current.to_frame().T)[0] if baseline is None else baseline[1]
        for idx in perm:
            f = features[idx]
            orig = current[f]
            current[f] = instance[f]
            pred = black_box.predict_proba(current.to_frame().T)[0][1] if hasattr(black_box, "predict_proba") else black_box.predict(current.to_frame().T)[0]
            marginal = pred - prev_pred
            phi[f] += marginal
            prev_pred = pred
    for f in features:
        phi[f] /= nsamples
    return phi

def find_counterfactual(black_box, instance: pd.Series, feature_steps: dict, target=None, max_iters=1000):
    if target is None:
        target = 1 - int(black_box.predict(instance.to_frame().T)[0])
    current = instance.copy()
    if black_box.predict(current.to_frame().T)[0] == target:
        return {"found": True, "instance": current, "changes": {}}
    features = list(feature_steps.keys())
    tried = set()
    queue = [(current.copy(), {})]
    it = 0
    while queue and it < max_iters:
        inst, changes = queue.pop(0)
        it += 1
        for f in features:
            for step in feature_steps[f]:
                new = inst.copy()
                new[f] = inst[f] + step
                key = tuple(sorted(changes.items()) + [(f, new[f])])
                if key in tried:
                    continue
                tried.add(key)
                pred = black_box.predict(new.to_frame().T)[0]
                new_changes = dict(changes)
                new_changes[f] = new[f]
                if pred == target:
                    return {"found": True, "instance": new, "changes": new_changes}
                queue.append((new, new_changes))
    return {"found": False, "instance": instance, "changes": {}}

def subgroup_divergence(black_box, X: pd.DataFrame, y: pd.Series, min_size=0.05, step_percentiles=[10,25,50,75,90]):
    results = []
    overall_acc = accuracy_score(y, black_box.predict(X))
    n = len(X)
    for col in X.columns:
        if np.issubdtype(X[col].dtype, np.number):
            vals = np.percentile(X[col], step_percentiles)
            for v in vals:
                subgroup_idx = X[X[col] <= v].index
                if len(subgroup_idx)/n < min_size or len(subgroup_idx) < 10:
                    continue
                sub_acc = accuracy_score(y.loc[subgroup_idx], black_box.predict(X.loc[subgroup_idx]))
                divergence = overall_acc - sub_acc
                results.append({"feature": col, "threshold": v, "size": len(subgroup_idx), "sub_acc": sub_acc, "overall_acc": overall_acc, "divergence": divergence})
        else:
            for val in X[col].unique():
                subgroup_idx = X[X[col] == val].index
                if len(subgroup_idx)/n < min_size or len(subgroup_idx) < 10:
                    continue
                sub_acc = accuracy_score(y.loc[subgroup_idx], black_box.predict(X.loc[subgroup_idx]))
                divergence = overall_acc - sub_acc
                results.append({"feature": col, "value": val, "size": len(subgroup_idx), "sub_acc": sub_acc, "overall_acc": overall_acc, "divergence": divergence})
    results.sort(key=lambda x: x["divergence"], reverse=True)
    return results

def export_global_explanation(surrogate: DecisionTreeClassifier, feature_names: List[str]) -> str:
    return export_text(surrogate, feature_names=feature_names)

def interactive_inspect(black_box, X, y, index):
    inst = X.iloc[index]
    pred = int(black_box.predict(inst.to_frame().T)[0])
    proba = black_box.predict_proba(inst.to_frame().T)[0] if hasattr(black_box, "predict_proba") else None
    return {"index": index, "instance": inst.to_dict(), "prediction": int(pred), "probability": proba}

def example_pipeline():
    np.random.seed(0)
    n = 1000
    X = pd.DataFrame({
        "credit_score": np.random.randint(300,850,n),
        "income": np.random.randint(20000,150000,n),
        "loan_amount": np.random.randint(1000,200000,n),
        "employment_years": np.random.randint(0,30,n),
        "dti": np.round(np.random.rand(n)*0.7,3)
    })
    y = (((X["credit_score"]>650) & (X["dti"]<0.4) & (X["employment_years"]>2)) | ((X["credit_score"]>750) & (X["loan_amount"]<100000))).astype(int)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    bb = fit_black_box(X_train, y_train)
    surrogate = train_global_surrogate(bb, X_train)
    global_text = export_global_explanation(surrogate, X_train.columns.tolist())
    inst = X_test.iloc[5]
    local = local_surrogate_explanation(bb, inst, X_train, n_samples=400)
    shap_vals = shap_monte_carlo(bb, inst, X_train, nsamples=300)
    cf = find_counterfactual(bb, inst, {"credit_score": [50,100,-50], "income":[10000,-10000], "dti":[-0.05,-0.1]}, target=1)
    sub_div = subgroup_divergence(bb, X_test, y_test)
    inspect = interactive_inspect(bb, X_test, y_test, 5)
    return {"global_tree": global_text, "local_linear": local, "shap": shap_vals, "counterfactual": cf, "subgroup_divergence": sub_div[:10], "inspect": inspect, "accuracy": accuracy_score(y_test, bb.predict(X_test))}

if __name__ == "__main__":
    out = example_pipeline()
    print(out["global_tree"])
    print("accuracy", out["accuracy"])
    print("local coefficients", out["local_linear"]["coefficients"])
    print("shap top", sorted(out["shap"].items(), key=lambda x: -abs(x[1]))[:5])
    print("counterfactual", out["counterfactual"]["found"], out["counterfactual"]["changes"])
    print("top subgroup divergences", out["subgroup_divergence"])
