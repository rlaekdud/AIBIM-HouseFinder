import styled from "styled-components";

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
  font-size: 1.8em;
  font-weight: bold;
  display: flex;
  justify-content: center;
  margin-bottom: 2%;
`;

const BluePrint = ({ item, onClick }) => {
  return (
    <Wrapper>
      <StyledSpan>{item}</StyledSpan>
      <StyledBluePrint
        onClick={() => onClick(item)}
        backgroundImg={`url(${require(`/Users/LEESEUNGYEOL/Desktop/AIBIM-HouseFinder/src/Img/${item}.png`)})`}
      />
    </Wrapper>
  );
};

export default BluePrint;
