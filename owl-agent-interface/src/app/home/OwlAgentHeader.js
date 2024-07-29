'use client';

import {
  Header,
  HeaderContainer,
  HeaderName,
  HeaderNavigation,
  HeaderMenuButton,
  HeaderMenuItem,
  HeaderGlobalBar,
  HeaderGlobalAction,
  SkipToContent,
  SideNav,
  SideNavItems,
  HeaderSideNavItems,
} from '@carbon/react';
import { Switcher, Notification, UserAvatar } from '@carbon/icons-react';

import Link from 'next/link';

const OwlAgentHeader = () => (
  <HeaderContainer
    render={({ isSideNavExpanded, onClickSideNavExpand }) => (
      <Header aria-label="Owl Agent">
        <SkipToContent />
        <HeaderMenuButton aria-label="Open menu" onClick={onClickSideNavExpand} isActive={isSideNavExpanded} />
        <Link href="/" passHref legacyBehavior>
          <HeaderName prefix="Athena">Owl Agent</HeaderName>
        </Link>
        <HeaderNavigation aria-label="Assistants">
          <Link href="/assistants" passHref legacyBehavior>
            <HeaderMenuItem>Assistants</HeaderMenuItem>
          </Link>
        </HeaderNavigation>
        <HeaderNavigation aria-label="Agents">
          <Link href="/agents" passHref legacyBehavior>
            <HeaderMenuItem>Agents</HeaderMenuItem>
          </Link>
        </HeaderNavigation>
        <HeaderNavigation aria-label="Tools">
          <Link href="/tools" passHref legacyBehavior>
            <HeaderMenuItem>Tools</HeaderMenuItem>
          </Link>
        </HeaderNavigation>
        <HeaderNavigation aria-label="Prompts">
          <Link href="/prompts" passHref legacyBehavior>
            <HeaderMenuItem>Prompts</HeaderMenuItem>
          </Link>
        </HeaderNavigation>
        <HeaderNavigation aria-label="Documents">
          <Link href="/documents" passHref legacyBehavior>
            <HeaderMenuItem>Documents</HeaderMenuItem>
          </Link>
        </HeaderNavigation>
        <SideNav aria-label="Side navigation" expanded={isSideNavExpanded} isPersistent={false} >
          <SideNavItems>
            <HeaderSideNavItems>
              <Link href="/assistants" passHref legacyBehavior>
                <HeaderMenuItem>Assistants</HeaderMenuItem>
              </Link>
              <Link href="/agents" passHref legacyBehavior>
                <HeaderMenuItem>Agents</HeaderMenuItem>
              </Link>
              <Link href="/tools" passHref legacyBehavior>
                <HeaderMenuItem>Tools</HeaderMenuItem>
              </Link>
              <Link href="/prompts" passHref legacyBehavior>
                <HeaderMenuItem>Prompts</HeaderMenuItem>
              </Link>
              <Link href="/documents" passHref legacyBehavior>
                <HeaderMenuItem>Documents</HeaderMenuItem>
              </Link>
            </HeaderSideNavItems>
          </SideNavItems>
        </SideNav>
        <HeaderGlobalBar>
          <HeaderGlobalAction aria-label="Notifications" tooltipAlignment="center" className="action-icons" >
            <Notification size={20} />
          </HeaderGlobalAction>
          <HeaderGlobalAction aria-label="User Avatar" tooltipAlignment="center" className="action-icons" >
            <UserAvatar size={20} />
          </HeaderGlobalAction>
          <HeaderGlobalAction aria-label="App Switcher" tooltipAlignment="end">
            <Switcher size={20} />
          </HeaderGlobalAction>
        </HeaderGlobalBar>
      </Header>
    )}
  />
);

export default OwlAgentHeader;
