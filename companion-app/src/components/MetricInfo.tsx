import React from "react";

type MetricInfoProps = {
  title: string;
  description?: string;
  showInfo: boolean;
  toggleInfo: () => void;
};

const MetricInfo = (props: MetricInfoProps) => {
  return (
    <>
      <div className="min-w-full rounded-lg border border-gray-200 bg-white p-6 shadow dark:border-gray-700 dark:bg-gray-800">
        <h5 className="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">
          {props.title}
        </h5>
        <p className="mb-3 font-normal text-gray-700 dark:text-gray-400">
          {props.description}
        </p>
        <button
          className="inline-flex items-center rounded-lg bg-blue-700 px-3 py-2 text-center text-sm font-medium text-white hover:bg-blue-800 focus:outline-none focus:ring-4 focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
          onClick={() => props.toggleInfo()}
        >
          {props.showInfo ? "Show Metric" : "Show Info"}
        </button>
      </div>
    </>
  );
};

export default MetricInfo;
