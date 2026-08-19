"use client";

import { useQuery } from "@tanstack/react-query";
import { get } from "@/services/api";
import { OverviewResponse } from "@/types";
import { KpiCard } from "@/components/KpiCard";
import { ChartCard } from "@/components/ChartCard";
import { LoadingState, ErrorState, EmptyState } from "@/components/States";

const RISK_COLORS: Record<string, string> = {
  Critical: "#dc2626",
  High: "#ea580c",
  Medium: "#d97706",
  Low: "#059669",
};

const RISK_LABELS_AR: Record<string, string> = {
  Critical: "حرج",
  High: "مرتفع",
  Medium: "متوسط",
  Low: "منخفض",
};

function formatCurrency(value: number) {
  return `${value.toLocaleString("en-US", { maximumFractionDigits: 0 })} د.ل`;
}

export default function OverviewPage() {
  const { data, isLoading, isError } = useQuery({
    queryKey: ["dashboard-overview"],
    queryFn: () => get<OverviewResponse>("/api/dashboard/overview"),
  });

  if (isLoading) return <LoadingState />;
  if (isError || !data) return <ErrorState />;

  const { kpis, charts } = data;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-slate-900">النظرة العامة التنفيذية</h1>
        <p className="text-sm text-slate-500">
          {data.model_version ? `إصدار النموذج: ${data.model_version}` : "لم يتم تشغيل التنبؤ بعد"}
        </p>
      </div>

      <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
        <KpiCard label="إجمالي العملاء النشطين" value={kpis.total_active_customers.toLocaleString("en-US")} />
        <KpiCard
          label="العملاء المتوقع تسربهم"
          value={kpis.predicted_churn_customers.toLocaleString("en-US")}
          sublabel={`${(kpis.predicted_churn_rate * 100).toFixed(1)}% من القاعدة`}
          tone="danger"
        />
        <KpiCard label="عملاء مخاطر مرتفعة" value={kpis.high_risk_customers.toLocaleString("en-US")} tone="warning" />
        <KpiCard label="عملاء مخاطر حرجة" value={kpis.critical_risk_customers.toLocaleString("en-US")} tone="danger" />
        <KpiCard label="الإيرادات المعرضة للخطر" value={formatCurrency(kpis.revenue_at_risk)} tone="danger" />
        <KpiCard
          label="متوسط احتمالية التسرب"
          value={`${(kpis.average_churn_probability * 100).toFixed(1)}%`}
        />
      </div>

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <ChartCard
          title="توزيع مستويات المخاطر"
          option={{
            tooltip: { trigger: "item" },
            legend: { bottom: 0, textStyle: { fontFamily: "var(--font-tajawal)" } },
            series: [
              {
                type: "pie",
                radius: ["45%", "75%"],
                data: charts.risk_distribution.map((d) => ({
                  name: RISK_LABELS_AR[d.level] ?? d.level,
                  value: d.count,
                  itemStyle: { color: RISK_COLORS[d.level] ?? "#94a3b8" },
                })),
                label: { formatter: "{b}: {c}" },
              },
            ],
          }}
        />

        <ChartCard
          title="معدل التسرب المتوقع حسب الخدمة"
          option={{
            tooltip: { trigger: "axis" },
            grid: { left: 40, right: 20, top: 20, bottom: 30 },
            xAxis: { type: "category", data: charts.churn_by_service.map((d) => d.category) },
            yAxis: { type: "value", axisLabel: { formatter: "{value}%" } },
            series: [
              {
                type: "bar",
                data: charts.churn_by_service.map((d) => +(d.churn_rate * 100).toFixed(1)),
                itemStyle: { color: "#0284c7", borderRadius: [4, 4, 0, 0] },
              },
            ],
          }}
        />

        <ChartCard
          title="معدل التسرب المتوقع حسب المنطقة"
          option={{
            tooltip: { trigger: "axis" },
            grid: { left: 40, right: 20, top: 20, bottom: 30 },
            xAxis: { type: "category", data: charts.churn_by_region.map((d) => d.category) },
            yAxis: { type: "value", axisLabel: { formatter: "{value}%" } },
            series: [
              {
                type: "bar",
                data: charts.churn_by_region.map((d) => +(d.churn_rate * 100).toFixed(1)),
                itemStyle: { color: "#7c3aed", borderRadius: [4, 4, 0, 0] },
              },
            ],
          }}
        />

        {charts.top_churn_drivers.length === 0 ? (
          <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
            <h3 className="mb-2 text-sm font-semibold text-slate-700">أهم أسباب التسرب</h3>
            <EmptyState />
          </div>
        ) : (
          <ChartCard
            title="أهم أسباب التسرب"
            option={{
              tooltip: { trigger: "axis" },
              grid: { left: 160, right: 20, top: 10, bottom: 10 },
              xAxis: { type: "value" },
              yAxis: {
                type: "category",
                data: charts.top_churn_drivers.map((d) => d.driver).reverse(),
                axisLabel: { fontFamily: "var(--font-tajawal)" },
              },
              series: [
                {
                  type: "bar",
                  data: charts.top_churn_drivers.map((d) => d.count).reverse(),
                  itemStyle: { color: "#db2777", borderRadius: [0, 4, 4, 0] },
                },
              ],
            }}
          />
        )}
      </div>
    </div>
  );
}
