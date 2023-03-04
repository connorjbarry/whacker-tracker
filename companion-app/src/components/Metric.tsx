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
      <div className="relative m-3 flex justify-between rounded-lg border border-[#C0C0C0] p-8">
        {showInfo ? (
          <MetricInfo title={props.title} description={props.desc} />
        ) : (
          <div className="relative flex h-full w-full justify-between">
            <p className="justify-start">{props.title}</p>
            <p className="mx-2 text-xl">
              <strong className="text-[#3A6EA5]">{props.metric}</strong>
            </p>
            <p className="justify-end uppercase tracking-widest">
              {props.units}
            </p>
          </div>
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
