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
  Stack,
} from '@carbon/react';
import { Notification, UserAvatar, Settings } from '@carbon/icons-react';

import Link from 'next/link';
import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import ReactMarkdown from 'react-markdown';
import { changeRole, context } from '../providers';

const languages = [{ text: "🇬🇧 English", value: "en" }, { text: "🇪🇸 Español", value: "es" }, { text: "🇫🇷 Français", value: "fr" }, { text: "🇳🇱 Nederlands", value: "nl" }];

const OwlAgentHeader = () => {
  const ctx = context();
  const role = ctx.role;
  const setRole = ctx.setRole;

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
          {(role === "admin" || role === "all") && <HeaderNavigation aria-label="Agents">
            <Link href="/agents" passHref legacyBehavior>
              <HeaderMenuItem>Agents</HeaderMenuItem>
            </Link>
          </HeaderNavigation>}
          {(role === "admin" || role === "all") && <HeaderNavigation aria-label="Tools">
            <Link href="/tools" passHref legacyBehavior>
              <HeaderMenuItem>Tools</HeaderMenuItem>
            </Link>
          </HeaderNavigation>}
          {(role === "admin" || role === "all") && <HeaderNavigation aria-label="Prompts">
            <Link href="/prompts" passHref legacyBehavior>
              <HeaderMenuItem>Prompts</HeaderMenuItem>
            </Link>
          </HeaderNavigation>}
          {(role === "admin" || role === "all") && <HeaderNavigation aria-label="Documents">
            <Link href="/documents" passHref legacyBehavior>
              <HeaderMenuItem>Documents</HeaderMenuItem>
            </Link>
          </HeaderNavigation>}
          {(role === "user" || role === "all") && <HeaderNavigation aria-label="Chatbot">
            <Link href="/owl" passHref legacyBehavior>
              <HeaderMenuItem>Chatbot</HeaderMenuItem>
            </Link>
          </HeaderNavigation>}

          <SideNav aria-label="Side navigation" expanded={isSideNavExpanded} isPersistent={false} >
            <SideNavItems>
              <HeaderSideNavItems>
                {(role === "admin" || role === "all") && <Link href="/agents" passHref legacyBehavior>
                  <HeaderMenuItem>Agents</HeaderMenuItem>
                </Link>}
                {(role === "admin" || role === "all") && <Link href="/tools" passHref legacyBehavior>
                  <HeaderMenuItem>Tools</HeaderMenuItem>
                </Link>}
                {(role === "admin" || role === "all") && <Link href="/prompts" passHref legacyBehavior>
                  <HeaderMenuItem>Prompts</HeaderMenuItem>
                </Link>}
                {(role === "admin" || role === "all") && <Link href="/documents" passHref legacyBehavior>
                  <HeaderMenuItem>Documents</HeaderMenuItem>
                </Link>}
                {(role === "user" || role === "all") && <Link href="/owl" passHref legacyBehavior>
                  <HeaderMenuItem>Chatbot</HeaderMenuItem>
                </Link>}
              </HeaderSideNavItems>
            </SideNavItems>
          </SideNav>

          <HeaderGlobalBar>
            <HeaderGlobalAction aria-label={t("header.alt.settings")} tooltipAlignment="center" className="action-icons"
              onClick={() => { setSettingsExpanded(!settingsExpanded); }}>
              <Settings size={20} />
            </HeaderGlobalAction>
            <HeaderGlobalAction aria-label={t("header.alt.notifications")} tooltipAlignment="center" className="action-icons" id="notifications-button">
              <Notification size={20} />
            </HeaderGlobalAction>
            <HeaderGlobalAction aria-label={t("header.alt.user")} tooltipAlignment="center" className="action-icons" >
              <UserAvatar size={20} />
            </HeaderGlobalAction>
          </HeaderGlobalBar>

          <HeaderPanel expanded={settingsExpanded}>
            <div className="header-panel-content">
              <h3>Configuration</h3>
              {/*<h3>{t('header.alt.configuration')}</h3>*/}
              <Stack gap={5}>
                <Dropdown id="role" titleText="Role" initialSelectedItem={role} label="Role" type="inline"
                  items={["admin", "user", "all"]}
                  onChange={(e) => { setRole(e.selectedItem) }} />
                <Dropdown id="language" titleText={t("header.lbl.language")} initialSelectedItem={languages.find((item) => (item.value === language))} label={t("header.lbl.language")} type="inline"
                  items={languages}
                  itemToString={item => item ? item.text : ""}
                  onChange={(e) => { changeLanguage(e.selectedItem.value) }} />
                {t('app.msg.welcome').split('\n').map((line, key) =>
                  line === "" ? <br key={key} /> :
                    <div key={key}>
                      <ReactMarkdown>{line}</ReactMarkdown>
                    </div>
                )}
                <p>Owl frontend v0.1</p>
              </Stack>
            </div>
          </HeaderPanel>
        </Header>
      )}
    />)
}

export default OwlAgentHeader;
