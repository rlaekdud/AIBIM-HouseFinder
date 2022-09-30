import React from "react";
import styled from "styled-components";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faTriangleExclamation } from "@fortawesome/free-solid-svg-icons";

const Wrapper = styled.div`
  width: 100%;
  height: 45vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
`;

const Span = styled.span`
  display: flex;
  text-align: center;
`;

const DataEmpty = () => {
  return (
    <Wrapper>
      <FontAwesomeIcon
        icon={faTriangleExclamation}
        size={"5x"}
        color={"#FFB456"}
        bounce={true}
      />
      <br />
      <Span>
        일치하는 데이터가 없습니다.
        <br />
        조건을 수정해주세요.
      </Span>
    </Wrapper>
  );
};
export default React.memo(DataEmpty);
