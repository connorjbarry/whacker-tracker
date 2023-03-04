import React from "react";

const ButtonGroup = ({ endSessionHandle, startSwingHandle }) => {
  return (
    <section className="text-black">
      <button
        className="m-4 rounded-lg border border-[#EBEBEB] bg-[#C0C0C0] p-4"
        onClick={endSessionHandle}
      >
        End Session
      </button>
      <button
        className="m-4 rounded-lg border border-[#EBEBEB] bg-[#C0C0C0] p-4"
        onClick={startSwingHandle}
      >
        Start Swing
      </button>
    </section>
  );
};

export default ButtonGroup;
