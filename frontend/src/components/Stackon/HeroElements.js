import styled from "styled-components";
import { Link as LinkS } from "react-scroll";

export const HeroContainer = styled.div`
  background: #0c0c0c;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0px 30px;
  height: 1700px;
  padding-top: 70px;
  position: relative;
  z-index: 1;

  @media screen and (min-height: 840px) {
    height: 1700px;
  }
  :before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(
        180deg,
        rgba(0, 0, 0, 0.2) 0%,
        rgba(0, 0, 0, 0.6) 100%
      ),
      linear-gradient(180deg, rgba(0, 0, 0, 0.2) 0%, transparent 100%);
    z-index: 2;
  }
`;

export const HeroBg = styled.div`
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
`;

export const VideoBg = styled.video`
  width: 100%;
  height: 100%;
  -o-object-fit: cover;
  object-fit: cover;
  background: #232a34;
`;

export const HeroContent = styled.div`
  z-index: 3;
  max-width: 1200px;
  position: absolute;
  padding: 8px 8px 24px 34px;
  display: flex;
  flex-direction: column;
  align-items: center;
`;

export const HeroH1 = styled.h1`
  color: white;
  font-size: 34px;
  text-align: center;

  @media screen and (max-width: 840px) {
    font-size: 20px;
  }

  @media screen and (max-width: 480px) {
    font-size: 26px;
  }
`;

export const HeroP = styled.p`
  margin-top: 24px;
  color: #fff;
  font-size: 24px;
  text-align: center;
  max-width: 600px;

  @media scrren and (max-width: 840px) {
    font-size: 24px;
  }

  @media screen and (max-width: 480px) {
    font-size: 18px;
  }
`;
export const HeroP2 = styled.p`
  margin-top: 24px;
  color: #fff;
  font-size: 16px;
  text-align: center;
  max-width: 600px;

  @media scrren and (max-width: 840px) {
    font-size: 16px;
  }

  @media screen and (max-width: 480px) {
    font-size: 14px;
  }
`;

export const ReviewSection = styled.div`
  bottom: 0;
  color: #fff;
  padding-bottom: 24px;
  position: absolute;
`;

export const ReviewWrapper = styled.div`
  display: inline-block;
  color: #fff;

  padding: 24px 24px;
`;

export const ReviewText = styled.p`
  text-align: center;
  font-size: 24px;
`;
export const UserInfo = styled.div`
  flex-direction: column;
  display: flex;
  padding-top: 12px;
  align-items: center;
  justify-content: center;
`;
export const UserDp = styled.img`
  width: 10%;
  padding-top: 24px;
  padding-right: 0;
  align-self: center;
`;
export const UserName = styled.h4`
  text-align: center;
`;
export const UserTitle = styled.h5`
  text-align: center;
`;

export const NavMenu = styled.ul`
  display: flex;
  align-items: center;
  list-style: none;
  text-align: center;
  margin-right: -22px;

  @media screen and (max-width: 840px) {
    display: none;
  }
`;

export const NavItem = styled.li`
  height: 80px;
`;

export const NavLinks = styled(LinkS)`
  color: #fff;
  display: flex;
  align-items: center;
  text-decoration: none;
  padding: 0 1rem;
  height: 100%;
  cursor: pointer;

  &.active {
    border-bottom: 3px solid #01bf71;
  }
  &:hover {
    color: #00bbf9;
    transition: 0.2s ease-in-out;
  }
`;

export const Table = styled.table`
  margin-left: auto;
  margin-right: auto;
  align-content: center;
  font-family: Arial, Helvetica, sans-serif;
  border-collapse: collapse;
  width: 40%;
`;

export const Td = styled.div`
  border: 3px solid #dddddd;
  text-align: left;
  padding: 8px;
`;

export const Tr = styled.div`
  :nth-child(even) {
    background-color: #dddddd;
  }
`;

export const TeamSec = styled.div`
  padding: 100px 0 160px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  background: #4b59f7;
`;

export const TeamWrapper = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 0 auto;

  @media screen and (max-width: 960px) {
    margin: 0 30px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
`;
export const VideoNFT = styled.video`
  width: 100%;
  height: 100%;
  -o-object-fit: cover;
  object-fit: cover;
  background: #232a34;
`;
export const TeamHeading = styled.h1`
  color: #fff;
  font-size: 48px;
  margin-bottom: 24px;
`;

export const TeamContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;

  @media screen and (max-width: 960px) {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 100%;
  }
`;

export const TeamCard = styled.div`
  background: transparent;
  box-shadow: 0 6px 20px rgba(56, 125, 255, 0.2);
  width: 250px;
  height: 500px;
  text-decoration: none;
  border-radius: 4px;
  margin: 14px;

  &:hover {
    transform: scale(1.06);
    transition: all 0.3s ease-out;
    color: #1c2237;
  }

  @media screen and (max-width: 960px) {
    width: 90%;

    &:hover {
      transform: none;
    }
  }
`;

export const TeamCardInfo = styled.div`
  display: flex;
  flex-direction: column;
  height: 450px;
  align-items: center;
  color: #fff;
`;

export const TeamName = styled.h3`
  margin: 5px 0;
  font-size: 18px;
`;

export const TeamTitle = styled.h4`
  font-size: 20px;
`;

export const ImgWrap = styled.div`
  max-width: 555px;
  height: 100%;
`;

export const Img = styled.img`
  width: 100%;
  height: 80%;
  padding-right: 0;
`;
export const SocialIcons = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 70px;
  margin-top: 5px;
`;

export const SocialIconLink = styled.a`
  color: #fff;
  font-size: 24px;
`;
