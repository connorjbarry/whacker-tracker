import React, { useState } from "react";
import { HiOutlineInformationCircle } from "react-icons/hi";
import MetricInfo from "./MetricInfo";

type MetricProps = {
  title: string;
  metric: string;
  units: string;
};

const Metric = (props: MetricProps) => {
  const [showInfo, setShowInfo] = useState(false);

  const showInfoModal = () => {
    setShowInfo(true);
  };

  const hideInfoModal = () => {
    setShowInfo(false);
  };

  return (
    <div className="relative m-4 flex justify-evenly rounded-lg border border-[#D8DBE2] p-8">
      <p className="">{props.title}</p>
      <p>
        <strong>{props.metric}</strong>
      </p>
      <p className="uppercase tracking-widest">{props.units}</p>
      <div
        className="absolute top-1 right-1 h-min w-min"
        onMouseEnter={showInfoModal}
        onMouseLeave={hideInfoModal}
      >
        <HiOutlineInformationCircle />
      </div>
      <div className="absolute -top-2 -right-28 z-10 h-auto w-auto rounded-lg bg-gray-300 ">
        {showInfo && <MetricInfo title={props.title} />}
      </div>
    </div>
  );
};

export default Metric;
