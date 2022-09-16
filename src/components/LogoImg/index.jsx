import React from "react";
import styled from "styled-components";

const Wrapper = styled.div`
  display: flex;
`;

const Section = styled.section`
  display: flex;
  align-items: center;
  justify-content: center;
`;

const LogoImg = () => {
  return (
    <Wrapper>
      <Section>
        <img src={require("../../Img/KNULOGO.png")} />
      </Section>
      <Section>
        <img
          src={require("../../Img/DADLLOGO.gif")}
          style={{ paddingLeft: "3.7em" }}
        />
      </Section>
      <Section>
        <img src={require("../../Img/IPALOGO.png")} />
      </Section>
    </Wrapper>
  );
};

export default React.memo(LogoImg);
