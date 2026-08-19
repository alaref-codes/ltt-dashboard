"use client";

import { useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import {
  createColumnHelper,
  flexRender,
  getCoreRowModel,
  useReactTable,
} from "@tanstack/react-table";
import Link from "next/link";
import { get } from "@/services/api";
import { CustomerRiskPage, CustomerRiskRow } from "@/types";
import { RiskBadge } from "@/components/RiskBadge";
import { LoadingState, ErrorState, EmptyState } from "@/components/States";

const SERVICES = ["4G LTE", "FWA", "ADSL", "VDSL", "FTTH"];
const REGIONS = ["West", "East", "South"];
const RISK_LEVELS = ["Critical", "High", "Medium", "Low"];

const columnHelper = createColumnHelper<CustomerRiskRow>();

function toCsv(rows: CustomerRiskRow[]): string {
  const headers = [
    "customer_id",
    "service_type",
    "region",
    "city",
    "arpu",
    "days_since_last_activity",
    "days_since_last_renewal",
    "usage_decline_pct",
    "number_of_complaints",
    "network_availability_pct",
    "churn_probability",
    "risk_score",
    "risk_level",
    "primary_driver",
  ];
  const lines = [headers.join(",")];
  for (const r of rows) {
    lines.push(
      headers
        .map((h) => {
          const value = (r as unknown as Record<string, unknown>)[h];
          const str = value === null || value === undefined ? "" : String(value);
          return `"${str.replace(/"/g, '""')}"`;
        })
        .join(",")
    );
  }
  return lines.join("\n");
}

function downloadCsv(rows: CustomerRiskRow[]) {
  const csv = toCsv(rows);
  const blob = new Blob(["﻿" + csv], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "customer_risk.csv";
  a.click();
  URL.revokeObjectURL(url);
}

export default function CustomersPage() {
  const [page, setPage] = useState(1);
  const [pageSize] = useState(25);
  const [search, setSearch] = useState("");
  const [region, setRegion] = useState("");
  const [serviceType, setServiceType] = useState("");
  const [riskLevel, setRiskLevel] = useState("");
  const [sortBy, setSortBy] = useState("risk_score");
  const [sortDir, setSortDir] = useState<"asc" | "desc">("desc");

  const params = new URLSearchParams({
    page: String(page),
    page_size: String(pageSize),
    sort_by: sortBy,
    sort_dir: sortDir,
  });
  if (search) params.set("search", search);
  if (region) params.set("region", region);
  if (serviceType) params.set("service_type", serviceType);
  if (riskLevel) params.set("risk_level", riskLevel);

  const { data, isLoading, isError } = useQuery({
    queryKey: ["customers", params.toString()],
    queryFn: () => get<CustomerRiskPage>(`/api/customers?${params.toString()}`),
    placeholderData: (prev) => prev,
  });

  const columns = useMemo(
    () => [
      columnHelper.accessor("customer_id", {
        header: "رقم العميل",
        cell: (info) => (
          <Link href={`/customers/${info.getValue()}`} className="font-medium text-sky-700 hover:underline">
            {info.getValue()}
          </Link>
        ),
      }),
      columnHelper.accessor("service_type", { header: "الخدمة" }),
      columnHelper.accessor("region", { header: "المنطقة" }),
      columnHelper.accessor("city", { header: "المدينة" }),
      columnHelper.accessor("arpu", {
        header: "ARPU",
        cell: (info) => info.getValue().toFixed(0),
      }),
      columnHelper.accessor("usage_decline_pct", {
        header: "انخفاض الاستخدام",
        cell: (info) => `${info.getValue().toFixed(0)}%`,
      }),
      columnHelper.accessor("number_of_complaints", { header: "الشكاوى" }),
      columnHelper.accessor("network_availability_pct", {
        header: "توفر الشبكة",
        cell: (info) => `${info.getValue().toFixed(1)}%`,
      }),
      columnHelper.accessor("churn_probability", {
        header: "احتمالية التسرب",
        cell: (info) => `${(info.getValue() * 100).toFixed(0)}%`,
      }),
      columnHelper.accessor("risk_level", {
        header: "مستوى المخاطرة",
        cell: (info) => <RiskBadge level={info.getValue()} />,
      }),
      columnHelper.accessor("primary_driver", {
        header: "السبب الرئيسي",
        cell: (info) => info.getValue() ?? "—",
      }),
    ],
    []
  );

  const table = useReactTable({
    data: data?.items ?? [],
    columns,
    getCoreRowModel: getCoreRowModel(),
    manualPagination: true,
    manualSorting: true,
    manualFiltering: true,
  });

  const totalPages = data ? Math.max(1, Math.ceil(data.total / data.page_size)) : 1;

  function toggleSort(columnId: string) {
    if (sortBy === columnId) {
      setSortDir((d) => (d === "asc" ? "desc" : "asc"));
    } else {
      setSortBy(columnId);
      setSortDir("desc");
    }
    setPage(1);
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-bold text-slate-900">تحليل مخاطر العملاء</h1>
        <button
          onClick={() => data && downloadCsv(data.items)}
          disabled={!data || data.items.length === 0}
          className="rounded-lg border border-slate-300 bg-white px-3 py-1.5 text-sm font-medium text-slate-700 hover:bg-slate-50 disabled:opacity-50"
        >
          تصدير CSV (الصفحة الحالية)
        </button>
      </div>

      <div className="flex flex-wrap gap-3 rounded-xl border border-slate-200 bg-white p-3">
        <input
          placeholder="بحث برقم العميل..."
          value={search}
          onChange={(e) => {
            setSearch(e.target.value);
            setPage(1);
          }}
          className="rounded-lg border border-slate-300 px-3 py-1.5 text-sm"
        />
        <select
          value={region}
          onChange={(e) => {
            setRegion(e.target.value);
            setPage(1);
          }}
          className="rounded-lg border border-slate-300 px-3 py-1.5 text-sm"
        >
          <option value="">كل المناطق</option>
          {REGIONS.map((r) => (
            <option key={r} value={r}>
              {r}
            </option>
          ))}
        </select>
        <select
          value={serviceType}
          onChange={(e) => {
            setServiceType(e.target.value);
            setPage(1);
          }}
          className="rounded-lg border border-slate-300 px-3 py-1.5 text-sm"
        >
          <option value="">كل الخدمات</option>
          {SERVICES.map((s) => (
            <option key={s} value={s}>
              {s}
            </option>
          ))}
        </select>
        <select
          value={riskLevel}
          onChange={(e) => {
            setRiskLevel(e.target.value);
            setPage(1);
          }}
          className="rounded-lg border border-slate-300 px-3 py-1.5 text-sm"
        >
          <option value="">كل مستويات المخاطرة</option>
          {RISK_LEVELS.map((l) => (
            <option key={l} value={l}>
              {l}
            </option>
          ))}
        </select>
      </div>

      {isLoading && !data ? (
        <LoadingState />
      ) : isError ? (
        <ErrorState />
      ) : !data || data.items.length === 0 ? (
        <EmptyState />
      ) : (
        <>
          <div className="overflow-x-auto rounded-xl border border-slate-200 bg-white">
            <table className="w-full text-right text-sm">
              <thead className="border-b border-slate-200 bg-slate-50">
                {table.getHeaderGroups().map((headerGroup) => (
                  <tr key={headerGroup.id}>
                    {headerGroup.headers.map((header) => (
                      <th
                        key={header.id}
                        onClick={() => toggleSort(header.column.id)}
                        className="cursor-pointer whitespace-nowrap px-3 py-2 font-semibold text-slate-600 select-none"
                      >
                        {flexRender(header.column.columnDef.header, header.getContext())}
                        {sortBy === header.column.id && (sortDir === "asc" ? " ▲" : " ▼")}
                      </th>
                    ))}
                  </tr>
                ))}
              </thead>
              <tbody>
                {table.getRowModel().rows.map((row) => (
                  <tr key={row.id} className="border-b border-slate-100 last:border-0 hover:bg-slate-50">
                    {row.getVisibleCells().map((cell) => (
                      <td key={cell.id} className="whitespace-nowrap px-3 py-2">
                        {flexRender(cell.column.columnDef.cell, cell.getContext())}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="flex items-center justify-between text-sm text-slate-600">
            <span>
              إجمالي النتائج: {data.total.toLocaleString("en-US")} — صفحة {page} من {totalPages}
            </span>
            <div className="flex gap-2">
              <button
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                disabled={page <= 1}
                className="rounded-lg border border-slate-300 bg-white px-3 py-1 disabled:opacity-40"
              >
                السابق
              </button>
              <button
                onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                disabled={page >= totalPages}
                className="rounded-lg border border-slate-300 bg-white px-3 py-1 disabled:opacity-40"
              >
                التالي
              </button>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
