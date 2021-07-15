import React, { useState } from "react";
import ListComponents from "./listComponents";
import {
  Button,
  Container,
  Form,
  H1,
  Heading,
  Input,
  Span,
  ListDiv,
} from "./listElements";

function List() {
  //collects characters inputted
  const [inputText, setInputText] = useState("");
  //collects characters added
  const [items, setItems] = useState([]);
  //second character collecter for second column
  const [items2, setItems2] = useState([]);

  function handleChange(event) {
    //getting hold of the input element
    var input = document.getElementById("input");
    const newValue = event.target.value;
    setInputText(newValue);
    //when enter is clicked item is added to list
    input.addEventListener("keydown", function (event) {
      if (event.keyCode === 13) {
        document.getElementById("button").click();
      }
    });
  }

  function addItem() {
    //function to ensure an input has been added (first if statement only)
    if (!inputText) {
      console.log("");
    } else {
      //if the function Allocation returns a true value items shall be added to the array
      if (!Allocation() === true) {
        setItems((prevItems) => {
          return [...prevItems, inputText];
        });
      }
      //if the function Allocation returns a true value items shall be added to the array
      if (Allocation() && Allocation2()) {
        setItems2((prevItems) => {
          return [...prevItems, inputText];
        });
      }

      //resets the input text so that it is always empty when a new item is to be added
      setInputText("");
    }
  }

  //deleting items of the list
  function onCheck(id, name) {
    //returns items to the array that fit the criteria name !== item[index]
    setItems((prevItems) => {
      return prevItems.filter((todoItem, index) => {
        return name !== items[index];
      });
    });
    //returns items to the array that fit the criteria name !== item[index] for second list
    setItems2((prevItems) => {
      return prevItems.filter((todoItem2, index) => {
        return name !== items2[index];
      });
    });
  }

  //allocating names to the two columns (validation)

  function Allocation() {
    if (items.length > 6) {
      return true;
    }
  }

  function Allocation2() {
    if (items2.length < 7) {
      return true;
    }
  }

  return (
    <Container className="container">
      <Form className="form">
        <Heading className="heading">
          <H1>Sport's hall sign-up list</H1>
        </Heading>
        <Input
          id="input"
          onChange={handleChange}
          type="text"
          value={inputText}
        />
        <Button id="button" onClick={addItem}>
          <Span>Add</Span>
        </Button>
        <ListDiv id="column1" style={{ float: "left" }}>
          {items.map((todoItem, index) => (
            <ListComponents
              onCheck={onCheck}
              name={todoItem}
              key={index}
              index={index}
            />
          ))}
        </ListDiv>

        <ListDiv id="column2" style={{ float: "right" }}>
          {items2.map((todoItem2, index) => (
            <ListComponents
              onCheck={onCheck}
              name={todoItem2}
              key={index}
              index={index}
            />
          ))}
        </ListDiv>
      </Form>
    </Container>
  );
}

export default List;
