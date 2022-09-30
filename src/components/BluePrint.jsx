import styled from "styled-components";
import React from "react";

const Wrapper = styled.div`
  width: 100%;
  height: 100%;
`;

const StyledBluePrint = styled.div`
  width: 100%;
  height: 90%;
  border: 2px solid;
  border-color: ${(props) => props.color};
  background-image: ${(props) => props.backgroundImg};
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  cursor: pointer;
  &:hover {
    opacity: 0.5;
  }

  color: ${(props) => props.color};
`;

const StyledSpan = styled.span`
  height: 10%;
  font-size: 1.6em;
  font-weight: bold;
  display: flex;
  justify-content: center;

  color: ${(props) => props.color};
`;

const BluePrint = ({ item, onClick, color }) => {
  return (
    <Wrapper>
      <StyledSpan color={color}>{item.floor_name}</StyledSpan>
      <StyledBluePrint
        onClick={() => onClick(item)}
        backgroundImg={`url("${item.floor_src}")`}
        color={color}
      />
    </Wrapper>
  );
};

export default React.memo(BluePrint);
