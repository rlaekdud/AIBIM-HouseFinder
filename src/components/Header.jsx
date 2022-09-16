import React from "react";
import styled from "styled-components";

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faHouseChimney } from "@fortawesome/free-solid-svg-icons";

const Wrapper = styled.div`
  display: flex;
  cursor: pointer;
`;

const LogoName = styled.div`
  padding: 0.02vw 0 0 1vw;

  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen,
    Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
  font-size: 3rem;
  font-weight: bolder;
`;

const Header = ({ onClick }) => {
  return (
    <Wrapper onClick={onClick}>
      <FontAwesomeIcon icon={faHouseChimney} size={"3x"} color="#002060" />
      <LogoName>AIBIM-HouseF!nder</LogoName>
    </Wrapper>
  );
};

export default React.memo(Header);
