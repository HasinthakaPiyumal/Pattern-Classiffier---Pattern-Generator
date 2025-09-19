import pandas as pd
import numpy as np
import datetime
import random

class CustomerActivitySimulator:
    def __init__(self, num_customers=100, start_date='2023-01-01', end_date='2023-03-31'):
        self.customers = [f'CUST{i:03d}' for i in range(num_customers)]
        self.products = [f'PROD{i:02d}' for i in range(20)]
        self.categories = ['Electronics', 'Clothing', 'Books', 'Home Goods', 'Groceries']
        self.start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        self.end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')

    def _generate_event(self, customer_id, current_date):
        event_type = random.choices(['view', 'add_to_cart', 'purchase'], weights=[0.6, 0.3, 0.1], k=1)[0]
        product_id = random.choice(self.products)
        category = random.choice(self.categories)
        price = round(random.uniform(10, 500), 2) if event_type == 'purchase' else 0
        return {
            'timestamp': current_date + datetime.timedelta(minutes=random.randint(0, 1440)),
            'customer_id': customer_id,
            'event_type': event_type,
            'product_id': product_id,
            'category': category,
            'price': price,
            'quantity': random.randint(1, 3) if event_type == 'purchase' else 0
        }

    def simulate_activities(self):
        all_activities = []
        current_date = self.start_date
        while current_date <= self.end_date:
            for customer_id in self.customers:
                if random.random() < 0.7:
                    num_events = random.randint(1, 5)
                    for _ in range(num_events):
                        all_activities.append(self._generate_event(customer_id, current_date))
            current_date += datetime.timedelta(days=1)
        return pd.DataFrame(all_activities)

class ChurnFeatureCollector:
    """
    Implements the Design Holistically pattern for E-commerce churn prediction.
    Data collection and initial feature extraction are designed together,
    anticipating the needs of a churn prediction model. This avoids a fragmented
    'pipeline jungle' by structuring data directly for ML-friendly insights.
    """
    def __init__(self, raw_data_df):
        self.raw_data = raw_data_df.sort_values(by=['customer_id', 'timestamp'])
        self.processed_data = None

    def _calculate_recency(self, customer_id, current_date):
        customer_purchases = self.raw_data[(self.raw_data['customer_id'] == customer_id) &
                                           (self.raw_data['event_type'] == 'purchase') &
                                           (self.raw_data['timestamp'] <= current_date)]
        if not customer_purchases.empty:
            last_purchase_date = customer_purchases['timestamp'].max()
            return (current_date - last_purchase_date).days
        return np.nan

    def _aggregate_customer_daily_features(self, customer_id, date):
        daily_events = self.raw_data[(self.raw_data['customer_id'] == customer_id) &
                                     (self.raw_data['timestamp'].dt.date == date.date())]
        daily_purchases = daily_events[daily_events['event_type'] == 'purchase']

        return {
            'customer_id': customer_id,
            'report_date': date,
            'total_views_daily': daily_events[daily_events['event_type'] == 'view'].shape[0],
            'total_purchases_daily': daily_purchases.shape[0],
            'total_spent_daily': daily_purchases['price'].sum(),
            'unique_categories_viewed_daily': daily_events['category'].nunique(),
            'has_activity_today': 1 if not daily_events.empty else 0
        }

    def collect_and_extract_holistically(self):
        print("Holistically collecting and extracting churn features...")
        customers = self.raw_data['customer_id'].unique()
        min_date = self.raw_data['timestamp'].min().date()
        max_date = self.raw_data['timestamp'].max().date()
        date_range = [min_date + datetime.timedelta(days=x) for x in range((max_date - min_date).days + 1)]

        all_customer_features = []
        for date in date_range:
            for cust_id in customers:
                daily_features = self._aggregate_customer_daily_features(cust_id, date)
                all_customer_features.append(daily_features)

        daily_features_df = pd.DataFrame(all_customer_features)

        print("Aggregating features over rolling windows...")
        final_features = []
        for cust_id in customers:
            customer_data = daily_features_df[daily_features_df['customer_id'] == cust_id].sort_values(by='report_date')
            if customer_data.empty:
                continue

            for i in range(len(customer_data)):
                current_date = customer_data.iloc[i]['report_date']
                window_start = current_date - datetime.timedelta(days=30)
                window_data = customer_data[(customer_data['report_date'] > window_start) &
                                            (customer_data['report_date'] <= current_date)]

                if window_data.empty:
                    continue

                features = {
                    'customer_id': cust_id,
                    'snapshot_date': current_date,
                    'total_spent_30d': window_data['total_spent_daily'].sum(),
                    'num_purchases_30d': window_data['total_purchases_daily'].sum(),
                    'num_views_30d': window_data['total_views_daily'].sum(),
                    'unique_categories_30d': window_data['unique_categories_viewed_daily'].apply(lambda x: x if x > 0 else np.nan).dropna().mean() if not window_data['unique_categories_viewed_daily'].empty else 0,
                    'activity_days_30d': window_data['has_activity_today'].sum(),
                    'recency_last_purchase_days': self._calculate_recency(cust_id, current_date)
                }
                final_features.append(features)

        self.processed_data = pd.DataFrame(final_features)
        return self.processed_data

if __name__ == '__main__':
    print("--- E-commerce Customer Churn Prediction (Holistic Design) ---")
    print("Simulating raw customer activities (representing initial data collection)...")
    simulator = CustomerActivitySimulator(num_customers=50, start_date='2023-01-01', end_date='2023-04-30')
    raw_activities_df = simulator.simulate_activities()
    print(f"Generated {raw_activities_df.shape[0]} raw activity records.")

    feature_collector = ChurnFeatureCollector(raw_activities_df)
    churn_features_df = feature_collector.collect_and_extract_holistically()

    print("\nHolistically Extracted Churn Features (first 5 rows):")
    print(churn_features_df.head())
    print(f"\nTotal churn feature snapshots generated: {churn_features_df.shape[0]}")
    print("\nThese features are now ready for a churn prediction model, avoiding a 'pipeline jungle'.")