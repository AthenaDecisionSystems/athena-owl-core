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
  HeaderPanel,
  Dropdown,
} from '@carbon/react';
import { Switcher, Notification, UserAvatar, Settings } from '@carbon/icons-react';

import Link from 'next/link';
import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import ReactMarkdown from 'react-markdown';

const languages = [{ text: "🇬🇧 English", value: "en" }, { text: "🇪🇸 Español", value: "es" }, { text: "🇫🇷 Français", value: "fr" }];

const OwlAgentHeader = () => {
  const [settingsExpanded, setSettingsExpanded] = useState(false);

  const { t, i18n } = useTranslation();
  const language = i18n.language;

  const changeLanguage = (language) => {
    i18n.changeLanguage(language);
    console.log('Language changed to', language);
  }

  return (
    <HeaderContainer
      render={({ isSideNavExpanded, onClickSideNavExpand }) => (
        <Header aria-label="Owl Agent">
          <SkipToContent />
          <HeaderMenuButton aria-label="Open menu" onClick={onClickSideNavExpand} isActive={isSideNavExpanded} />
          <Link href="/" passHref legacyBehavior>
            <HeaderName prefix="Athena">Owl Agent</HeaderName>
          </Link>
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
            <HeaderGlobalAction aria-label="Settings" tooltipAlignment="center" className="action-icons"
              onClick={() => { setSettingsExpanded(!settingsExpanded); }}>
              <Settings size={20} />
            </HeaderGlobalAction>
            <HeaderGlobalAction aria-label="Notifications" tooltipAlignment="center" className="action-icons" id="notifications-button">
              <Notification size={20} />
            </HeaderGlobalAction>
            <HeaderGlobalAction aria-label="User Avatar" tooltipAlignment="center" className="action-icons" >
              <UserAvatar size={20} />
            </HeaderGlobalAction>
          </HeaderGlobalBar>

          <HeaderPanel expanded={settingsExpanded}>
            <div className="header-panel-content">
              <h3>{t('app.alt.configuration')}</h3>
              <Dropdown id="language" titleText="Language" initialSelectedItem={languages.find((item) => (item.value === language))} label="Language" type="inline"
                items={languages}
                itemToString={item => item ? item.text : ""}
                onChange={(e) => { changeLanguage(e.selectedItem.value) }} />
              {t('app.msg.welcome').split('\n').map((line, key) =>
                line === "" ? <br key={key} /> :
                  <div key={key}>
                    <ReactMarkdown>{line}</ReactMarkdown>
                  </div>
              )}
            </div>
          </HeaderPanel>
        </Header>
      )}
    />)
}

export default OwlAgentHeader;
