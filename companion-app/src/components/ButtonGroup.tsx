import React from "react";

const ButtonGroup = ({ endSessionHandle, startSwingHandle }) => {
  return (
    <section className="mt-4 flex justify-between text-black">
      <button
        className="inline-flex  items-center rounded-lg bg-blue-700 px-3 py-2 text-center text-sm font-medium text-white hover:bg-blue-800 focus:outline-none focus:ring-4 focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800 "
        onClick={endSessionHandle}
      >
        End Session
      </button>
      <div className="mx-4" />
      <button
        className="inline-flex  items-center rounded-lg bg-blue-700 px-3 py-2 text-center text-sm font-medium text-white hover:bg-blue-800 focus:outline-none focus:ring-4 focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800 "
        onClick={startSwingHandle}
      >
        Start Swing
      </button>
    </section>
  );
};

export default ButtonGroup;
