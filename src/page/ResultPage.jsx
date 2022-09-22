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
  height: 85%;
`;
const HeaderSection = styled.section`
  width: 100%;
  height: 10%;

  margin-bottom: 3%;
  display: flex;
  justify-content: space-between;
`;

const ImgSection = styled.section`
  width: 100%;
  height: 70%;
  display: flex;
  justify-content: space-around;
`;

const Span = styled.span`
  font-size: 2.3em;
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
const BtnSection = styled.div`
  width: 18%;
  margin-top: 2%;
  display: flex;
  justify-content: space-between;
`;

const OtherFloorSection = styled.div`
  width: 47%;

  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-gap: 3%;
`;

const BottomSection = styled.div`
  width: 100%;
  height: 20%;
  margin-top: 6%;

  display: flex;
  justify-content: space-between;
`;

const dummyData = ["18-235-1", "18-235-1", "18-235-1"];

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
        <HeaderSection>
          <div style={{ display: "flex", flexDirection: "column", gap: "40%" }}>
            <Span
              style={{
                color: "#002060",
                fontWeight: "bold",
              }}
            >
              House Drawing
            </Span>
            <Span style={{ fontSize: "1.7em" }}>{resultData}</Span>
          </div>
          <BtnSection>
            <Btn
              width={"4em"}
              height={"2em"}
              onClick={() => {}}
              item={"Main"}
              borderRadius={"10px"}
            />
            <Btn
              width={"4em"}
              height={"2em"}
              onClick={() => {}}
              item={"Sub"}
              backgroundColor={"#F3C73C"}
              borderRadius={"10px"}
            />
          </BtnSection>
        </HeaderSection>
        <ImgSection>
          <div
            style={{
              width: "35%",
            }}
          >
            <CenterSection>
              <SmallSpan color={"#002060"}>Floor Plan</SmallSpan>
            </CenterSection>
            <ImgDiv
              backgroundImg={`url(${require(`/Users/LEESEUNGYEOL/Desktop/AIBIM-HouseFinder/src/Img/${resultData}.png`)})`}
            ></ImgDiv>
          </div>
          <div style={{ borderLeft: "2px solid gray", height: "70vh" }}></div>
          <div
            style={{
              width: "35%",
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
        <BottomSection>
          <OtherFloorSection>
            {dummyData.map((it) => {
              return (
                <ImgDiv
                  backgroundImg={`url(${require(`/Users/LEESEUNGYEOL/Desktop/AIBIM-HouseFinder/src/Img/${it}.png`)})`}
                ></ImgDiv>
              );
            })}
          </OtherFloorSection>
          <div style={{ marginTop: "5%" }}>
            <Btn
              width={"4em"}
              height={"2em"}
              onClick={() => navigator(-1)}
              item={"Back"}
              borderRadius={"10px"}
            />
          </div>
        </BottomSection>
      </Section>
    </Wrapper>
  );
};

export default React.memo(ResultPage);
