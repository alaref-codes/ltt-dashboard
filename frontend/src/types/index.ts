export interface Driver {
  feature: string;
  description: string;
  category: string;
}

export interface Prediction {
  churn_probability: number;
  risk_score: number;
  risk_level: "Low" | "Medium" | "High" | "Critical" | "Unscored";
  top_drivers: Driver[];
  recommended_action: string;
  prediction_date: string;
  model_version: string;
}

export interface CustomerRiskRow {
  customer_id: string;
  service_type: string;
  region: string;
  city: string;
  arpu: number;
  days_since_last_activity: number;
  days_since_last_renewal: number;
  usage_decline_pct: number;
  number_of_complaints: number;
  network_availability_pct: number;
  churn_probability: number;
  risk_score: number;
  risk_level: string;
  primary_driver: string | null;
}

export interface CustomerRiskPage {
  items: CustomerRiskRow[];
  total: number;
  page: number;
  page_size: number;
}

export interface CustomerSummary {
  customer_id: string;
  subscriber_id: string;
  account_id: string;
  city: string;
  region: string;
  customer_type: string;
  registration_date: string;
  activation_date: string;
}

export interface SubscriptionInfo {
  service_type: string;
  package_name: string;
  subscription_status: string;
  activation_date: string;
  expiration_date: string;
  last_renewal_date: string;
  number_of_renewals: number;
}

export interface UsageInfo {
  daily_usage_gb: number;
  weekly_usage_gb: number;
  monthly_usage_gb: number;
  usage_last_7d_gb: number;
  usage_last_30d_gb: number;
  usage_last_90d_gb: number;
  usage_trend: string;
  usage_decline_pct: number;
  days_since_last_activity: number;
}

export interface PaymentInfo {
  monthly_revenue: number;
  arpu: number;
  recharge_value: number;
  recharge_frequency: number;
  failed_payments: number;
  outstanding_balance: number;
  revenue_trend: string;
}

export interface ComplaintInfo {
  number_of_complaints: number;
  complaint_type: string;
  open_complaints: number;
  average_resolution_time_hours: number;
  last_complaint_date: string | null;
}

export interface NetworkInfo {
  network_availability_pct: number;
  number_of_outages: number;
  total_downtime_hours: number;
  average_downtime_hours: number;
  repeated_outages: number;
  average_speed_mbps: number;
  latency_ms: number;
  service_area: string;
}

export interface CustomerProfile {
  customer: CustomerSummary;
  subscription: SubscriptionInfo;
  usage: UsageInfo;
  payment: PaymentInfo;
  complaint: ComplaintInfo;
  network: NetworkInfo;
  prediction: Prediction | null;
}

export interface OverviewKpis {
  total_active_customers: number;
  predicted_churn_customers: number;
  predicted_churn_rate: number;
  high_risk_customers: number;
  critical_risk_customers: number;
  revenue_at_risk: number;
  average_churn_probability: number;
}

export interface RiskDistributionItem {
  level: string;
  count: number;
}

export interface ChurnByCategoryItem {
  category: string;
  churn_rate: number;
  count: number;
  revenue_at_risk: number;
}

export interface DriverCountItem {
  driver: string;
  count: number;
}

export interface OverviewResponse {
  kpis: OverviewKpis;
  charts: {
    risk_distribution: RiskDistributionItem[];
    churn_by_service: ChurnByCategoryItem[];
    churn_by_region: ChurnByCategoryItem[];
    top_churn_drivers: DriverCountItem[];
  };
  model_version: string | null;
}

export interface AuthUser {
  full_name: string;
  role: string;
}
