import React from "react";
import { useNavigate } from "react-router-dom";
import styled from "styled-components";

//components
import Header from "../components/Header";
import Footer from "../components/Footer";
import LogoImg from "../components/LogoImg/index";
import Btn from "../components/Btn/index";

const Wrapper = styled.div`
  width: 100%;
  height: 100%;
`;
const Section = styled.section`
  width: 100%;
  height: 90%;
  display: flex;
  align-items: center;
  justify-content: center;
`;
const BottomSection = styled.section`
  padding: 3rem 1rem;
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
`;

const LandingPage = ({ handleReset }) => {
  const navigate = useNavigate();
  return (
    <Wrapper>
      <Section>
        <div>
          <Header />
          <div
            style={{
              display: "flex",
              justifyContent: "center",
              marginTop: "5em",
            }}
          >
            <Btn
              width="5em"
              height="1.8em"
              item="Start"
              fontSize="2em"
              borderRadius={"20px"}
              onClick={() => {
                alert(
                  "시범 운행중입니다.\n개선사항이 있으시면 gpwls3143@gmail.com로 연락주세요."
                );
                handleReset();
                navigate("/main");
              }}
            />
          </div>
        </div>
      </Section>
      <BottomSection>
        <Footer />
        <LogoImg />
      </BottomSection>
    </Wrapper>
  );
};
export default React.memo(LandingPage);
