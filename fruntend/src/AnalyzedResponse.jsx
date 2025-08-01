import { useDispatch, useSelector } from "react-redux";
import { onback } from "./redux/apiSlice";
import back_arrow from "./assets/back_arrow.svg";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";

const AnalyzedResponse = () => {
  const { gimini_data, loading, error, state_linkedin } = useSelector(
    (state) => state.storerd
  );
  const dispatch = useDispatch();

  if (loading)
    return (
      <p className="flex justify-center m-5 font-bold items-center">
        Please wait, loading data...
      </p>
    );
  if (error) return <p className="text-red-500">{error}</p>;
  if (!gimini_data || !gimini_data.response)
    return <p>No analysis data found.</p>;

  let data;
  try {
    data = JSON.parse(gimini_data.response);
    console.log(data);
  } catch (e) {
    console.log(data);
    console.log(gimini_data.response);
    return (
      <div className="text-center text-red-600 mt-8">
        Error parsing analysis data.
      </div>
    );
  }

  const getColor = (score) => {
    if (score >= 80) return "text-green-600";
    if (score >= 50) return "text-yellow-500";
    return "text-red-500";
  };

  const chartData = Object.entries(data.section_scores).map(
    ([section, score]) => ({
      name: section,
      score,
    })
  );

  const chartColors = [
    "#4CAF50", // green
    "#2196F3", // blue
    "#FF9800", // orange
    "#F44336", // red
    "#9C27B0", // purple
    "#009688", // teal
  ];

  return (
    <div className="max-w-6xl mx-auto p-6 space-y-10 font-sans">
      <div className="flex justify-between items-center">
        <img
          src={back_arrow}
          onClick={() => dispatch(onback())}
          alt="Back"
          className="w-8 h-8 cursor-pointer"
        />
        <h1 className="text-3xl md:text-4xl font-bold text-blue-800 drop-shadow-sm pr-5">
          {state_linkedin ? "LinkedIn" : "Resume"} Analysis
        </h1>
        <div></div>
      </div>

      {/* ATS Summary */}
      <div className="bg-gradient-to-r from-indigo-100 to-white p-6 rounded-2xl shadow">
        <p className="text-2xl font-semibold text-gray-800">
          ATS Score:{" "}
          <span className={`font-bold ${getColor(data.ats_score)}`}>
            {data.ats_score}
          </span>
        </p>
        <p className="mt-3 text-gray-700 text-base leading-relaxed">
          {data.summary}
        </p>
      </div>

      {/* Sections Lists */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <ListCard
          title="🔍 Suggestions"
          color="blue"
          items={data.suggestions}
        />
        <ListCard title="✅ Strengths" color="green" items={data.strengths} />
        <ListCard
          title="⚠️ Weak Sections"
          color="red"
          items={data.weak_sections}
        />
        <ListCard
          title="📌 Missing Keywords"
          color="yellow"
          items={data.missing_keywords}
        />
        <ListCard
          title="🧾 Formatting Issues"
          color="purple"
          items={data.formatting_issues}
        />
      </div>

      {/* Bar Chart Section */}
      <div className="bg-white p-6 rounded-2xl shadow-md">
        <h2 className="text-2xl font-semibold text-gray-800 mb-4 flex items-center">
          📊 Section Scores
        </h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart
            data={chartData}
            margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" style={{ fontSize: "14px" }} />
            <YAxis />
            <Tooltip />
            <Bar dataKey="score" radius={[10, 10, 0, 0]}>
              {chartData.map((_, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={chartColors[index % chartColors.length]}
                />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

// ListCard reusable component
const ListCard = ({ title, items, color }) => {
  const titleColor = {
    blue: "text-blue-600",
    green: "text-green-600",
    red: "text-red-600",
    yellow: "text-yellow-600",
    purple: "text-purple-600",
  }[color];

  return (
    <div className="bg-white p-5 rounded-2xl shadow-md">
      <h3 className={`text-xl font-semibold mb-3 ${titleColor}`}>{title}</h3>
      <ul className="list-disc list-inside space-y-2 text-gray-700 text-sm">
        {items?.length ? (
          items.map((item, idx) => <li key={idx}>{item}</li>)
        ) : (
          <li className="text-gray-400 italic">No data available.</li>
        )}
      </ul>
    </div>
  );
};

export default AnalyzedResponse;
