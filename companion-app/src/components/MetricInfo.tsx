import React from "react";

type MetricInfoProps = {
  title: string;
  description?: string;
};

const MetricInfo = (props: MetricInfoProps) => {
  return (
    <>
      <div className="flex uppercase">{props.description} </div>
    </>
  );
};

export default MetricInfo;
