/**
 * @license
 * Copyright 2025 AionUi (aionui.com)
 * SPDX-License-Identifier: Apache-2.0
 */

import { ConfigStorage } from '@/common/storage';
import AionScrollArea from '@/renderer/components/base/AionScrollArea';
import { useThemeContext } from '@/renderer/context/ThemeContext';
import { Button, Divider, Form, Input, Message, Select, Alert } from '@arco-design/web-react';
import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import classNames from 'classnames';
import { useSettingsViewMode } from '../settingsViewContext';

interface CodeBuddyModalContentProps {
  /** 请求关闭设置弹窗 / Request closing the settings modal */
  onRequestClose?: () => void;
}

const CodeBuddyModalContent: React.FC<CodeBuddyModalContentProps> = ({ onRequestClose }) => {
  const { t } = useTranslation();
  const { theme: _theme } = useThemeContext();
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [message, messageContext] = Message.useMessage();
  const viewMode = useSettingsViewMode();
  const isPageMode = viewMode === 'page';

  const onSubmit = async () => {
    try {
      const values = await form.validate();
      setLoading(true);

      const codebuddyConfig = {
        CODEBUDDY_API_KEY: values.CODEBUDDY_API_KEY || '',
        CODEBUDDY_INTERNET_ENVIRONMENT: values.CODEBUDDY_INTERNET_ENVIRONMENT || 'overseas',
      };

      await ConfigStorage.set('codebuddy.config', codebuddyConfig);

      message.success(t('common.saveSuccess'));
      onRequestClose?.();
    } catch (error: unknown) {
      message.error((error as Error)?.message || t('common.saveFailed'));
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    onRequestClose?.();
  };

  useEffect(() => {
    ConfigStorage.get('codebuddy.config')
      .then((codebuddyConfig) => {
        const formData = {
          CODEBUDDY_API_KEY: codebuddyConfig?.CODEBUDDY_API_KEY || '',
          CODEBUDDY_INTERNET_ENVIRONMENT: codebuddyConfig?.CODEBUDDY_INTERNET_ENVIRONMENT || 'overseas',
        };
        form.setFieldsValue(formData);
      })
      .catch((error) => {
        console.error('Failed to load CodeBuddy configuration:', error);
      });
  }, []);

  return (
    <div className='flex flex-col h-full w-full'>
      {messageContext}

      {/* Content Area */}
      <AionScrollArea className='flex-1 min-h-0' disableOverflow={isPageMode}>
        <div className='space-y-16px'>
          {/* Alert Information */}
          <div className='px-[12px] py-[24px] md:px-[32px]'>
            <Alert
              type='info'
              title={t('settings.codeBuddyInfo', { defaultValue: 'CodeBuddy Configuration Information' })}
              content={t('settings.codeBuddyInfoDescription', {
                defaultValue:
                  'Configure your CodeBuddy API Key and internet environment. The API Key is required for authentication. The internet environment determines which CodeBuddy service you are using (Overseas, China, or iOA).',
              })}
            />
          </div>

          {/* Configuration Form */}
          <div className='px-[12px] py-[24px] md:px-[32px] bg-2 rd-12px md:rd-16px border border-border-2'>
            <Form form={form} layout='horizontal' labelCol={{ flex: '180px' }} labelAlign='left' wrapperCol={{ flex: '1' }}>
              {/* API Key Field */}
              <Form.Item
                label={t('settings.codeBuddyApiKey', { defaultValue: 'API Key' })}
                field='CODEBUDDY_API_KEY'
                layout='vertical'
                rules={[
                  {
                    required: false,
                  },
                ]}
              >
                <Input
                  className='aion-input'
                  type='password'
                  placeholder={t('settings.codeBuddyApiKeyPlaceholder', {
                    defaultValue: 'Enter your CodeBuddy API Key from https://www.codebuddy.ai/profile/keys',
                  })}
                />
              </Form.Item>

              <Divider className='mt-0px mb-20px' />

              {/* Internet Environment Field */}
              <Form.Item
                label={t('settings.codeBuddyInternetEnvironment', { defaultValue: 'Internet Environment' })}
                field='CODEBUDDY_INTERNET_ENVIRONMENT'
                layout='vertical'
                rules={[
                  {
                    required: true,
                  },
                ]}
              >
                <Select
                  placeholder={t('settings.codeBuddySelectEnvironment', {
                    defaultValue: 'Select your CodeBuddy service region',
                  })}
                  options={[
                    {
                      label: t('settings.codeBuddyOverseas', {
                        defaultValue: 'Overseas (www.codebuddy.ai)',
                      }),
                      value: 'overseas',
                    },
                    {
                      label: t('settings.codeBuddyChina', {
                        defaultValue: 'China (copilot.tencent.com)',
                      }),
                      value: 'internal',
                    },
                    {
                      label: t('settings.codeBuddyIOA', {
                        defaultValue: 'iOA (tencent.sso.copilot.tencent.com)',
                      }),
                      value: 'ioa',
                    },
                  ]}
                />
              </Form.Item>

              <Divider className='mt-0px mb-20px' />

              {/* Info Section */}
              <div className='text-12px text-t-secondary space-y-8px'>
                <div>
                  <div className='font-600 mb-4px'>
                    {t('settings.codeBuddyApiKeyInfo', { defaultValue: 'How to get your API Key:' })}
                  </div>
                  <ul className='list-disc list-inside space-y-4px'>
                    <li>
                      {t('settings.codeBuddyOverseasKey', { defaultValue: 'Overseas:' })}{' '}
                      <a
                        href='https://www.codebuddy.ai/profile/keys'
                        target='_blank'
                        rel='noreferrer'
                        className='text-t-primary hover:underline'
                      >
                        https://www.codebuddy.ai/profile/keys
                      </a>
                    </li>
                    <li>
                      {t('settings.codeBuddyChinaKey', { defaultValue: 'China:' })}{' '}
                      <a
                        href='https://copilot.tencent.com/profile/'
                        target='_blank'
                        rel='noreferrer'
                        className='text-t-primary hover:underline'
                      >
                        https://copilot.tencent.com/profile/
                      </a>
                    </li>
                    <li>
                      {t('settings.codeBuddyIOAKey', { defaultValue: 'iOA:' })}{' '}
                      <a
                        href='https://tencent.sso.copilot.tencent.com/profile/keys'
                        target='_blank'
                        rel='noreferrer'
                        className='text-t-primary hover:underline'
                      >
                        https://tencent.sso.copilot.tencent.com/profile/keys
                      </a>
                    </li>
                  </ul>
                </div>
              </div>
            </Form>
          </div>
        </div>
      </AionScrollArea>

      {/* Footer with Buttons */}
      <div className={classNames('shrink-0 flex gap-10px border-t border-border-2 pl-24px py-16px', isPageMode ? 'border-none pl-0 pr-0 pt-10px flex-col md:flex-row md:justify-end' : 'justify-end')}>
        <Button className={classNames('rd-100px', isPageMode && 'w-full md:w-auto')} onClick={handleCancel}>
          {t('common.cancel')}
        </Button>
        <Button type='primary' loading={loading} onClick={onSubmit} className={classNames('rd-100px', isPageMode && 'w-full md:w-auto')}>
          {t('common.save')}
        </Button>
      </div>
    </div>
  );
};

export default CodeBuddyModalContent;
