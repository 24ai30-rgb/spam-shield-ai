"use client";

import { Bar, BarChart, CartesianGrid, Cell, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { verdictColor } from "@/lib/utils";

export function VerdictDistributionChart({ data }: { data: Record<string, number> }) {
  const chartData = Object.entries(data).map(([label, value]) => ({
    name: label.replace("_", " "),
    value,
    color: verdictColor[label as keyof typeof verdictColor] || "#8894AA",
  }));

  if (chartData.length === 0) {
    return <p className="text-sm text-fog-400 py-8 text-center">No scan data yet.</p>;
  }

  return (
    <ResponsiveContainer width="100%" height={220}>
      <PieChart>
        <Pie data={chartData} dataKey="value" nameKey="name" innerRadius={55} outerRadius={85} paddingAngle={3}>
          {chartData.map((entry, i) => (
            <Cell key={i} fill={entry.color} stroke="none" />
          ))}
        </Pie>
        <Tooltip
          contentStyle={{ background: "#141B2D", border: "none", borderRadius: 8, fontSize: 12 }}
          itemStyle={{ color: "#EDF1F7" }}
        />
      </PieChart>
    </ResponsiveContainer>
  );
}

export function CategoryBreakdownChart({ data }: { data: Record<string, number> }) {
  const chartData = Object.entries(data).map(([name, value]) => ({ name, value }));

  if (chartData.length === 0) {
    return <p className="text-sm text-fog-400 py-8 text-center">No category data yet.</p>;
  }

  return (
    <ResponsiveContainer width="100%" height={240}>
      <BarChart data={chartData} layout="vertical" margin={{ left: 20 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#8894AA22" horizontal={false} />
        <XAxis type="number" tick={{ fontSize: 11, fill: "#8894AA" }} axisLine={false} tickLine={false} />
        <YAxis
          type="category"
          dataKey="name"
          width={140}
          tick={{ fontSize: 11, fill: "#8894AA" }}
          axisLine={false}
          tickLine={false}
        />
        <Tooltip contentStyle={{ background: "#141B2D", border: "none", borderRadius: 8, fontSize: 12 }} />
        <Bar dataKey="value" fill="#FFB020" radius={[0, 6, 6, 0]} barSize={16} />
      </BarChart>
    </ResponsiveContainer>
  );
}
