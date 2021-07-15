import React from "react";
import SignUp from "../signUp";

function Hero() {
  return (
    <div style={{ backgroundColor: "#95e1d3", height: "100vh" }}>
      <h1 style={{ margin: 0, textAlign: "center", padding: "2rem 0 2rem" }}>Sign Up sheet</h1>
      <SignUp />
    </div>
  );
}

export default Hero;
