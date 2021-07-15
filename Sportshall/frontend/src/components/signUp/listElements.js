import styled from "styled-components";

export const Container = styled.div`
  display: flex;
  justify-content: center;
`;

export const Heading = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
`;

export const H1 = styled.h1`
  transform: rotate(2deg);
  padding: 0.2rem 1.2rem;
  border-radius: 20% 5% 20% 5%/5% 20% 25% 20%;
  background-color: #95e1d3;
  font-size: 1.5rem;
`;

export const Form = styled.div`
  width: 100%;
  height: auto;
  max-width: 70vw;
  min-width: 250px;
  max-height: auto;
  min-height: 500px;
  background: #f1f5f8;
  background-image: radial-gradient(#bfc0c1 7.2%, transparent 0);
  background-size: 25px 25px;
  border-radius: 20px;
  box-shadow: 4px 3px 7px 2px #00000040;
  padding: 1rem;
  box-sizing: border-box;
`;

export const Input = styled.input`
  box-sizing: border-box;
  background-color: transparent;
  padding: 0.7rem;
  border-bottom-right-radius: 15px 3px;
  border-bottom-left-radius: 3px 15px;
  border: solid 3px transparent;
  border-bottom: dashed 3px #95e1d3;
  font-family: "Architects Daughter", cursive;
  font-size: 1rem;
  color: hsla(260, 2%, 25%, 0.7);
  width: 75%;
  margin-bottom: 20px;
`;

export const Button = styled.button`
  padding: 0;
  border: none;
  font-family: "Architects Daughter", cursive;
  text-decoration: none;
  padding-bottom: 3px;
  border-radius: 5px;
  background-color: #95e1d3;
`;

export const Span = styled.span`
  background: #f1f5f8;
  display: block;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  border: 1px solid hsl(198, 1%, 29%);
`;

export const ListDiv = styled.div`
  width: 50%;
`;

export const Li = styled.div`
  font-size: 20px;
  max-height: 300px;
  width: 100%;
  margin: 10px 0 10px 0rem;
  &:hover {
    text-decoration: line-through;
    cursor: pointer;
  }
`;
