import React from "react";

type MetricInfoProps = {
  title: string;
  description?: string;
};

const MetricInfo = (props: MetricInfoProps) => {
  return <div className="p-2">{props.title}</div>;
};

export default MetricInfo;
