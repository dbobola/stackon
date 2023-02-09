import React, { useState, useEffect } from "react";
import { FaBars } from "react-icons/fa";
import { IconContext } from "react-icons/lib";
import { animateScroll as scroll } from "react-scroll";

import {
  NavbarContainer,
  Nav,
  NavLogo,
  MobileIcon,
  // HeroBtnWrapper,
  // FormContent,
  //  FormInput,
  NavBtn,
  NavBtnLink,
} from "./NavbarElements";

const Navbar = ({ toggle, disabled = true }) => {
  const [scrollNav, setScrollNav] = useState(false);
  const changeNav = () => {
    if (window.scrollY >= 80) {
      setScrollNav(true);
    } else {
      setScrollNav(false);
    }
  };
  useEffect(() => {
    window.addEventListener("scroll", changeNav);
  }, []);
  const toggleHome = () => {
    scroll.scrollToTop();
  };

  return (
    <>
      <IconContext.Provider value={{ color: "#fff" }}>
        <Nav scrollNav={scrollNav}>
          <NavbarContainer>
            <NavLogo to="/" onClick={toggleHome}>
              Stackon
            </NavLogo>
            <MobileIcon onClick={toggle}>
              <FaBars />
            </MobileIcon>

            <NavBtn>
              <NavBtnLink
                to=""
                smooth={true}
                duration={500}
                spy={true}
                exact="true"
                offset={-80}
              >
                Connect Wallet
              </NavBtnLink>
            </NavBtn>
          </NavbarContainer>
        </Nav>
      </IconContext.Provider>
    </>
  );
};

export default Navbar;
