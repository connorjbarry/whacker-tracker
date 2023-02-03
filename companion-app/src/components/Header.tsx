import React, { useRef, useState } from "react";

const Header = () => {
  const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  const titleRef = useRef<HTMLHeadingElement>();
  const [iterations, setIterations] = useState(0);

  const changeText = () => {
    const title = titleRef.current;
    let iteration = iterations;
    const interval = setInterval(() => {
      title.innerHTML = title?.innerHTML
        .split("")
        .map((letter, idx) => {
          if (idx < iterations) {
            return title?.dataset.value[idx];
          }
          return letters[Math.floor(Math.random() * letters.length)];
        })
        .join("");

      if (iterations === title?.dataset.value?.length) {
        clearInterval(interval);
        setIterations(0);
      }

      setIterations(() => (iteration += 1 / 3));
      console.log(iterations);
    }, 50);
  };

  return (
    <h1
      className="betwe mt-8 text-5xl uppercase text-white"
      ref={titleRef}
      data-value="Whacker Tracker"
      onMouseEnter={() => changeText()}
    >
      Whacker Tracker
    </h1>
  );
};

export default Header;
