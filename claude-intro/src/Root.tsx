import React from 'react';
import {Composition} from 'remotion';
import {ClaudeIntro, TOTAL_FRAMES} from './Video';

export const Root: React.FC = () => (
  <Composition id="ClaudeIntro" component={ClaudeIntro} durationInFrames={TOTAL_FRAMES} fps={30} width={720} height={1280} />
);
