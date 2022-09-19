import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import styled from "styled-components";

//components
import Btn from "../components/Btn";

// styled component
const Wrapper = styled.div`
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
`;
const Section = styled.section`
  width: 80%;
  height: 80%;
`;
const HeaderSection = styled.section`
  width: 100%;
  height: 15%;
  margin-top: 2%;
  display: flex;
  justify-content: space-between;
`;

const ImgSection = styled.section`
  width: 100%;
  height: 75%;
  display: flex;
  justify-content: space-around;
`;

const Span = styled.span`
  font-size: 2.5em;
  font-weight: "bold";
`;

const SmallSpan = styled.span`
  font-weight: bold;
  font-size: 1.5rem;
  color: ${(props) => (props.color ? props.color : "black")};
`;
const CenterSection = styled.section`
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 3%;
`;

const ImgDiv = styled.div`
  height: 100%;
  border: 2px solid black;
  background-image: ${(props) => props.backgroundImg};
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
`;

const ResultPage = ({ resultData }) => {
  const navigator = useNavigate();

  // useEffect(() => {
  //   const result = require("child_process").spawn("py", ["test.py"]);
  //   result.stdout.on("data", function (data) {
  //     console.log(data.toString());
  //   });
  // }, []);
  return (
    <Wrapper>
      <Section>
        <Span
          style={{
            color: "#002060",
            marginBottom: "3%",
            fontWeight: "bold",
          }}
        >
          House`s Floor Plan
        </Span>
        <HeaderSection>
          <Span>{resultData}</Span>
          <Btn
            width={"7%"}
            height={"50%"}
            onClick={() => navigator(-1)}
            item={"Back"}
          />
        </HeaderSection>
        <div></div>
        <ImgSection>
          <div
            style={{
              width: "33%",
            }}
          >
            <CenterSection>
              <SmallSpan color={"#002060"}>Floor Plan</SmallSpan>
            </CenterSection>
            <ImgDiv
              backgroundImg={`url(${require(`/Users/LEESEUNGYEOL/Desktop/AIBIM-HouseFinder/src/Img/${resultData}.png`)})`}
            ></ImgDiv>
          </div>
          <div
            style={{
              width: "33%",
            }}
          >
            <CenterSection>
              <SmallSpan color={"#002060"}>Space Diagram</SmallSpan>
            </CenterSection>
            <ImgDiv
              backgroundImg={`url(${require(`/Users/LEESEUNGYEOL/Desktop/AIBIM-HouseFinder/src/Img/${resultData}.jpg`)})`}
            ></ImgDiv>
          </div>
        </ImgSection>
      </Section>
    </Wrapper>
  );
};

export default React.memo(ResultPage);
