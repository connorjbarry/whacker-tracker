import React, { useState } from "react";
import { HiOutlineInformationCircle } from "react-icons/hi";
import { RxCross2 } from "react-icons/rx";
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
      <div className="relative m-4 flex justify-evenly rounded-lg border border-[#D8DBE2] p-8">
        {showInfo ? (
          <MetricInfo title={props.title} description={props.desc} />
        ) : (
          <>
            <p className="">{props.title}</p>
            <p>
              <strong>{props.metric}</strong>
            </p>
            <p className="uppercase tracking-widest">{props.units}</p>
          </>
        )}

        <div
          className="absolute top-1 right-1 h-min w-min cursor-pointer"
          onClick={() => toggleInfoModal()}
        >
          {showInfo ? <RxCross2 /> : <HiOutlineInformationCircle />}
        </div>
      </div>
    </>
  );
};

export default Metric;
