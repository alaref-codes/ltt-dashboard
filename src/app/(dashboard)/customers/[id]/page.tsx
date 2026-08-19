"use client";

import { use } from "react";
import { useQuery } from "@tanstack/react-query";
import Link from "next/link";
import { get } from "@/services/api";
import { CustomerProfile } from "@/types";
import { RiskBadge } from "@/components/RiskBadge";
import { LoadingState, ErrorState } from "@/components/States";

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
      <h3 className="mb-3 text-sm font-semibold text-slate-700">{title}</h3>
      {children}
    </div>
  );
}

function Field({ label, value }: { label: string; value: React.ReactNode }) {
  return (
    <div className="flex items-center justify-between border-b border-slate-100 py-1.5 text-sm last:border-0">
      <span className="text-slate-500">{label}</span>
      <span className="font-medium text-slate-800">{value}</span>
    </div>
  );
}

export default function CustomerProfilePage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);

  const { data, isLoading, isError } = useQuery({
    queryKey: ["customer", id],
    queryFn: () => get<CustomerProfile>(`/api/customers/${id}`),
  });

  if (isLoading) return <LoadingState />;
  if (isError || !data) return <ErrorState message="تعذر العثور على بيانات العميل" />;

  const { customer, subscription, usage, payment, complaint, network, prediction } = data;

  return (
    <div className="space-y-6">
      <div>
        <Link href="/customers" className="text-sm text-sky-700 hover:underline">
          ← العودة إلى قائمة العملاء
        </Link>
        <div className="mt-2 flex items-center gap-3">
          <h1 className="text-xl font-bold text-slate-900">{customer.customer_id}</h1>
          {prediction && <RiskBadge level={prediction.risk_level} />}
        </div>
        <p className="text-sm text-slate-500">
          {customer.city} — {customer.region} — {customer.customer_type}
        </p>
      </div>

      {prediction && (
        <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
          <div className="mb-3 flex flex-wrap items-center justify-between gap-2">
            <div>
              <p className="text-sm text-slate-500">احتمالية التسرب</p>
              <p className="text-2xl font-bold text-red-600">{(prediction.churn_probability * 100).toFixed(0)}%</p>
            </div>
            <div className="rounded-lg bg-sky-50 px-4 py-2 text-sm text-sky-800">
              <span className="font-semibold">الإجراء الموصى به: </span>
              {prediction.recommended_action}
            </div>
          </div>
          <p className="mb-2 text-sm font-semibold text-slate-600">أهم أسباب الخطر:</p>
          <ul className="list-inside list-disc space-y-1 text-sm text-slate-700">
            {prediction.top_drivers.length === 0 && <li className="text-slate-400">لا توجد عوامل خطر بارزة</li>}
            {prediction.top_drivers.map((d, i) => (
              <li key={i}>{d.description}</li>
            ))}
          </ul>
        </div>
      )}

      <div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3">
        <Section title="بيانات الاشتراك">
          <Field label="الخدمة" value={subscription.service_type} />
          <Field label="الباقة" value={subscription.package_name} />
          <Field label="الحالة" value={subscription.subscription_status} />
          <Field label="تاريخ آخر تجديد" value={subscription.last_renewal_date} />
          <Field label="تاريخ الانتهاء" value={subscription.expiration_date} />
          <Field label="عدد مرات التجديد" value={subscription.number_of_renewals} />
        </Section>

        <Section title="الاستخدام">
          <Field label="آخر 30 يوم (جيجابايت)" value={usage.usage_last_30d_gb.toFixed(1)} />
          <Field label="آخر 90 يوم (جيجابايت)" value={usage.usage_last_90d_gb.toFixed(1)} />
          <Field label="اتجاه الاستخدام" value={usage.usage_trend} />
          <Field label="نسبة الانخفاض" value={`${usage.usage_decline_pct.toFixed(0)}%`} />
          <Field label="أيام منذ آخر نشاط" value={usage.days_since_last_activity} />
        </Section>

        <Section title="الإيرادات والدفع">
          <Field label="ARPU" value={payment.arpu.toFixed(0)} />
          <Field label="الإيراد الشهري" value={payment.monthly_revenue.toFixed(0)} />
          <Field label="اتجاه الإيراد" value={payment.revenue_trend} />
          <Field label="محاولات دفع فاشلة" value={payment.failed_payments} />
          <Field label="رصيد مستحق" value={payment.outstanding_balance.toFixed(0)} />
        </Section>

        <Section title="الشكاوى">
          <Field label="عدد الشكاوى" value={complaint.number_of_complaints} />
          <Field label="شكاوى مفتوحة" value={complaint.open_complaints} />
          <Field label="نوع الشكوى" value={complaint.complaint_type} />
          <Field label="متوسط وقت الحل (ساعة)" value={complaint.average_resolution_time_hours.toFixed(0)} />
          <Field label="تاريخ آخر شكوى" value={complaint.last_complaint_date ?? "—"} />
        </Section>

        <Section title="تجربة الشبكة">
          <Field label="توفر الشبكة" value={`${network.network_availability_pct.toFixed(1)}%`} />
          <Field label="عدد الانقطاعات" value={network.number_of_outages} />
          <Field label="ساعات الانقطاع" value={network.total_downtime_hours.toFixed(1)} />
          <Field label="متوسط السرعة (ميجابت)" value={network.average_speed_mbps.toFixed(0)} />
          <Field label="زمن الاستجابة (مللي ثانية)" value={network.latency_ms.toFixed(0)} />
        </Section>

        <Section title="بيانات العميل">
          <Field label="رقم المشترك" value={customer.subscriber_id} />
          <Field label="رقم الحساب" value={customer.account_id} />
          <Field label="تاريخ التسجيل" value={customer.registration_date} />
          <Field label="تاريخ التفعيل" value={customer.activation_date} />
        </Section>
      </div>
    </div>
  );
}
