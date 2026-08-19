"use client";

import ReactECharts from "echarts-for-react";
import { EChartsOption } from "echarts";

export function ChartCard({
  title,
  option,
  height = 280,
}: {
  title: string;
  option: EChartsOption;
  height?: number;
}) {
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
      <h3 className="mb-2 text-sm font-semibold text-slate-700">{title}</h3>
      <ReactECharts option={option} style={{ height }} notMerge lazyUpdate />
    </div>
  );
}
