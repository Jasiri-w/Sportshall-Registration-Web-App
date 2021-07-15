import React from "react";
import { Li } from "./listElements";

function ListComponent(props) {
  return (
    <>
      <Li
        onClick={() => {
          props.onCheck(props.index, props.name);
        }}
      >
        {props.name}
      </Li>
    </>
  );
}

export default ListComponent;
