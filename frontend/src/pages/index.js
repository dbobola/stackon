import React, { useState } from "react";
import Stackon from "../components/Stackon";
import Navbar from "../components/Navbar";
// import GetData from "../components/Stackon/getData";

const Home = () => {
  const [isOpen, setIsOpen] = useState(false);
  const toggle = () => {
    setIsOpen(!isOpen);
  };
  return (
    <>
      <Navbar toggle={toggle} />
      <Stackon />
    </>
  );
};

export default Home;
