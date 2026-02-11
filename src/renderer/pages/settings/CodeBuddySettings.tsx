/**
 * @license
 * Copyright 2025 AionUi (aionui.com)
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import CodeBuddyModalContent from '@/renderer/components/SettingsModal/contents/CodeBuddyModalContent';
import SettingsPageWrapper from './components/SettingsPageWrapper';

const CodeBuddySettings: React.FC = () => {
  return (
    <SettingsPageWrapper>
      <CodeBuddyModalContent />
    </SettingsPageWrapper>
  );
};

export default CodeBuddySettings;
