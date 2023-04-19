import { type NextPage } from "next";
import Head from "next/head";
import Header from "../components/Header";
import Metric from "../components/Metric";
import { socket } from "../utils/socket";
import { useEffect, useState } from "react";
import SwingPath from "../components/SwingPath";
import { io } from "socket.io-client";
// import Link from "next/link";

// import { api } from "../utils/api";

const metrics = {
  club_speed: {
    title: "Club Head Speed",
    metric: "0",
    units: "MPH",
    desc: "Speed of the club head at impact",
  },
  club_angle: {
    title: "Club Face Angle",
    metric: "0",
    units: "Deg",
    desc: "Angle of the club face at impact",
  },

  ball_speed: {
    title: "Ball Speed",
    metric: "0",
    units: "MPH",
    desc: "Speed of the ball at impact",
  },
  ball_distance: {
    title: "Ball Distance",
    metric: "0",
    units: "Yds",
    desc: "Distance the ball traveled",
  },
  smash_factor: {
    title: "Smash Factor",
    metric: "0",
    units: "",
    desc: "Ratio of ball speed to club speed",
  },
  launch_angle: {
    title: "Launch Angle",
    metric: "0",
    units: "Deg",
    desc: "Angle of the ball at launch",
  },
};

const Home: NextPage = () => {
  // const hello = api.example.hello.useQuery({ text: "from tRPC" });

  const [data, setData] = useState({});

  useEffect(() => {
    console.log("hey");
    const socket = io("http://localhost:5000", {
      transports: ["websocket"],
      multiplex: false,
    });
    socket.on("connect", () => {
      console.log("connected");
      socket.emit("detection", "hello world");
    });
    socket.onAny((event, ...args) => {
      console.log(event, args);
      if (event === "metrics") {
        setData(args[0]);
        socket.emit("detection", "hello world");
      }
    });
    return () => {
      socket.off("connect");
    };
  }, []);

  return (
    <>
      <Head>
        <title>Whacker Tracker</title>
        <meta name="description" content="Purdue ECE Capstone Project" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <main className="flex h-screen flex-col items-center justify-center text-center">
        <Header />
        {/* <ButtonGroup
          endSessionHandle={endSessionHandle}
          startSwingHandle={startSwingHandle}
        /> */}
        <div className="grid h-4/5 w-full items-center justify-center px-6 xl:grid-cols-2">
          <section className="grid w-full items-center justify-center md:grid-cols-2">
            {Object.entries(metrics).map(([key, value]) => (
              <Metric
                key={key}
                title={value.title}
                metric={data[key] || value.metric}
                units={value.units}
                desc={value.desc}
              />
            ))}
          </section>
          <section>
            <SwingPath />
          </section>
        </div>
      </main>
    </>
  );
};

export default Home;
