import React from "react";
import styled from "styled-components";

// styled components
const StyledBtn = styled.button`
  height: ${(props) => props.height};
  width: ${(props) => props.width};
  border-radius: ${(props) =>
    props.borderRadius ? props.borderRadius : "1.2rem"};
  background-color: ${(props) =>
    props.backgroundColor ? props.backgroundColor : "#002060"};
  color: ${(props) => (props.color ? props.color : "white")};

  display: flex;
  align-items: center;
  justify-content: center;
  font-size: ${(props) => (props.fontSize ? props.fontSize : "1.3rem")};
  border: 1px solid white;
  box-shadow: 0.8rem 0.5rem 1.4rem #bec5d0, -0.3rem -0.4rem 0.8rem #fbfbfb;
  user-select: none;

  &:active {
    box-shadow: inset -0.3rem -0.1rem 1.4rem #fbfbfb,
      inset 0.3rem 0.4rem 0.8rem #bec5d0;
    cursor: pointer;
  }
  &:hover {
    cursor: pointer;
  }
`;

//conponent

const Btn = ({
  onClick,
  item,
  width,
  height,
  borderRadius,
  backgroundColor,
  color,
  fontSize,
}) => {
  return (
    <StyledBtn
      onClick={onClick}
      width={width}
      height={height}
      borderRadius={borderRadius}
      backgroundColor={backgroundColor}
      color={color}
      fontSize={fontSize}
    >
      {item}
    </StyledBtn>
  );
};
export default React.memo(Btn);
