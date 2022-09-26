import styled from "styled-components";
import React from "react";

const Wrapper = styled.div`
  width: 100%;
  height: 100%;
`;

const StyledBluePrint = styled.div`
  width: 100%;
  height: 100%;
  border: 2px solid black;
  margin-bottom: 3%;
  background-image: ${(props) => props.backgroundImg};
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  cursor: pointer;
`;

const StyledSpan = styled.span`
  font-size: 1.6em;
  font-weight: bold;
  display: flex;
  justify-content: center;
  margin-bottom: 2%;
`;

const BluePrint = ({ item, onClick }) => {
  return (
    <Wrapper>
      <StyledSpan>{item.floor_name}</StyledSpan>
      <StyledBluePrint
        onClick={() => onClick(item)}
        backgroundImg={`url("${item.floor_src}")`}
      />
    </Wrapper>
  );
};

export default React.memo(BluePrint);
