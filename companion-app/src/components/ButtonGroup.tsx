import React from "react";

const ButtonGroup = ({ endSessionHandle, startSwingHandle }) => {
  return (
    <section className="text-black">
      <button
        className="m-4 rounded-lg border border-[#D8DBE2] bg-[#F9FAFB] p-4"
        onClick={endSessionHandle}
      >
        End Session
      </button>
      <button
        className="m-4 rounded-lg border border-[#D8DBE2] bg-[#F9FAFB] p-4"
        onClick={startSwingHandle}
      >
        Start Swing
      </button>
    </section>
  );
};

export default ButtonGroup;
