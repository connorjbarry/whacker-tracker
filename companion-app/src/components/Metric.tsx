import React, { useState } from "react";
import MetricInfo from "./MetricInfo";

type MetricProps = {
  title: string;
  metric: string;
  units: string;
  desc: string;
};

const Metric = (props: MetricProps) => {
  const [showInfo, setShowInfo] = useState(false);

  const toggleInfoModal = () => {
    setShowInfo(() => !showInfo);
  };

  return (
    <>
      <div className=" m-3 flex h-full w-full justify-between p-2">
        {showInfo ? (
          <MetricInfo
            title={props.title}
            description={props.desc}
            showInfo={showInfo}
            toggleInfo={() => toggleInfoModal()}
          />
        ) : (
          <div className=" min-w-full rounded-lg border border-gray-200 bg-white p-4 shadow dark:border-gray-700 dark:bg-gray-800">
            <h5 className="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">
              {props.title}
            </h5>
            <p className="mb-3 font-normal text-gray-700 dark:text-gray-400">
              <b>{props.metric}</b> {props.units}
            </p>
            <button
              className="inline-flex max-w-fit items-center rounded-lg bg-blue-700 px-3 py-2 text-center text-sm font-medium text-white hover:bg-blue-800 focus:outline-none focus:ring-4 focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800 "
              onClick={() => toggleInfoModal()}
            >
              {showInfo ? "Show Metric" : "Show Info"}
            </button>
          </div>
        )}
      </div>
    </>
  );
};

export default Metric;
