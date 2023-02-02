import React from "react";
import styled from "styled-components";

const Wrapper = styled.div`
  display: flex;
`;

// const Section = styled.section`
//   display: flex;
//   align-items: center;
//   justify-content: center;
// `;

const LogoImg = () => {
  return (
    <Wrapper>
      <img
        src={require("../../Img/KNULOGO.png")}
        style={{ width: "12vw", objectFit: "contain" }}
      />

      <div
        style={{
          width: "13vw",
          backgroundImage: `url(${require("../../Img/DADLLOGO.gif")})`,
          backgroundSize: "contain",
          backgroundRepeat: "no-repeat",
          backgroundPosition: "center",
          marginLeft: "10%",
        }}
      ></div>

      <img
        src={require("../../Img/IPALOGO.png")}
        style={{ width: "12vw", objectFit: "contain" }}
      />
    </Wrapper>
  );
};

export default React.memo(LogoImg);
