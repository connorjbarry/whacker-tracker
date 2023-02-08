import React, { useEffect, useRef, useState } from "react";

const Header = () => {
  const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  const titleRef = useRef<HTMLHeadingElement>();

  const changeText = (iteration: number) => {
    const title = titleRef.current;
    const interval = setInterval(() => {
      title.innerHTML = title?.innerHTML
        .split("")
        .map((letter, idx) => {
          if (idx < iteration) {
            return title?.dataset.value[idx];
          }
          return letters[Math.floor(Math.random() * letters.length)];
        })
        .join("");

      if (iteration === title?.dataset.value?.length) {
        clearInterval(interval);
        iteration = 0;
      }

      iteration += 1 / 3;
    }, 60);
  };

  useEffect(() => {
    let iteration = 0;
    changeText(iteration);
    iteration = 0;
  }, []);

  return (
    <h1
      className="text-5xl uppercase tracking-widest text-white"
      ref={titleRef}
      data-value="Whacker Tracker"
    >
      Whacker Tracker
    </h1>
  );
};

export default Header;
