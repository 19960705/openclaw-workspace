import React, { useState } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  Modal,
  Pressable,
} from 'react-native';
import { Mood, Efficiency } from '../../types';
import {
  COLORS,
  MOOD_EMOJIS,
  MOOD_LABELS,
  ENERGY_EMOJIS,
  ENERGY_LABELS,
  EFFICIENCY_EMOJIS,
  EFFICIENCY_LABELS,
} from '../../constants';

interface CheckInModalProps {
  visible: boolean;
  onClose: () => void;
  onSubmit: (mood: Mood, energy: 1 | 2 | 3 | 4, efficiency: Efficiency) => void;
}

const STEPS = ['mood', 'energy', 'efficiency'] as const;

export const CheckInModal: React.FC<CheckInModalProps> = ({
  visible,
  onClose,
  onSubmit,
}) => {
  const [step, setStep] = useState(0);
  const [mood, setMood] = useState<Mood | null>(null);
  const [energy, setEnergy] = useState<1 | 2 | 3 | 4 | null>(null);
  const [efficiency, setEfficiency] = useState<Efficiency | null>(null);

  const handleNext = () => {
    if (step < STEPS.length - 1) {
      setStep(step + 1);
    }
  };

  const handleBack = () => {
    if (step > 0) {
      setStep(step - 1);
    } else {
      handleClose();
    }
  };

  const handleClose = () => {
    setStep(0);
    setMood(null);
    setEnergy(null);
    setEfficiency(null);
    onClose();
  };

  const handleSubmit = () => {
    if (mood && energy && efficiency) {
      onSubmit(mood, energy, efficiency);
      handleClose();
    }
  };

  const renderStep = () => {
    switch (STEPS[step]) {
      case 'mood':
        return (
          <View style={styles.stepContainer}>
            <Text style={styles.stepTitle}>今天状态如何？</Text>
            <Text style={styles.stepSubtitle}>选择最能描述你的表情</Text>
            <View style={styles.emojiRow}>
              {(['happy', 'okay', 'tired', 'crashed'] as Mood[]).map(m => (
                <TouchableOpacity
                  key={m}
                  style={[
                    styles.emojiButton,
                    mood === m && styles.emojiButtonSelected,
                  ]}
                  onPress={() => setMood(m)}
                  activeOpacity={0.7}
                >
                  <Text style={styles.emoji}>{MOOD_EMOJIS[m]}</Text>
                  <Text style={styles.emojiLabel}>{MOOD_LABELS[m]}</Text>
                </TouchableOpacity>
              ))}
            </View>
          </View>
        );

      case 'energy':
        return (
          <View style={styles.stepContainer}>
            <Text style={styles.stepTitle}>精力值多少？</Text>
            <Text style={styles.stepSubtitle}>🔋 代表你的能量水平</Text>
            <View style={styles.energyRow}>
              {([1, 2, 3, 4] as const).map(e => (
                <TouchableOpacity
                  key={e}
                  style={[
                    styles.energyButton,
                    energy === e && styles.energyButtonSelected,
                  ]}
                  onPress={() => setEnergy(e)}
                  activeOpacity={0.7}
                >
                  <Text style={styles.energyEmoji}>{ENERGY_EMOJIS[e]}</Text>
                  <Text style={styles.energyLabel}>{ENERGY_LABELS[e]}</Text>
                </TouchableOpacity>
              ))}
            </View>
          </View>
        );

      case 'efficiency':
        return (
          <View style={styles.stepContainer}>
            <Text style={styles.stepTitle}>工作效率如何？</Text>
            <Text style={styles.stepSubtitle}>对自己诚实，没关系的</Text>
            <View style={styles.efficiencyRow}>
              {(['high', 'medium', 'low'] as Efficiency[]).map(e => (
                <TouchableOpacity
                  key={e}
                  style={[
                    styles.efficiencyButton,
                    efficiency === e && styles.efficiencyButtonSelected,
                  ]}
                  onPress={() => setEfficiency(e)}
                  activeOpacity={0.7}
                >
                  <Text style={styles.efficiencyEmoji}>{EFFICIENCY_EMOJIS[e]}</Text>
                  <Text style={styles.efficiencyLabel}>{EFFICIENCY_LABELS[e]}</Text>
                </TouchableOpacity>
              ))}
            </View>
          </View>
        );
    }
  };

  const canProceed = () => {
    switch (step) {
      case 0:
        return mood !== null;
      case 1:
        return energy !== null;
      case 2:
        return efficiency !== null;
      default:
        return false;
    }
  };

  return (
    <Modal
      visible={visible}
      animationType="slide"
      presentationStyle="pageSheet"
      onRequestClose={handleClose}
    >
      <View style={styles.container}>
        {/* Header */}
        <View style={styles.header}>
          <TouchableOpacity onPress={handleBack} style={styles.backButton}>
            <Text style={styles.backText}>
              {step === 0 ? '取消' : '← 上一步'}
            </Text>
          </TouchableOpacity>
          <View style={styles.progressBar}>
            <View
              style={[styles.progressFill, { width: `${((step + 1) / 3) * 100}%` }]}
            />
          </View>
          <TouchableOpacity
            onPress={step === 2 ? handleSubmit : handleNext}
            style={[
              styles.nextButton,
              !canProceed() && styles.nextButtonDisabled,
            ]}
            disabled={!canProceed()}
          >
            <Text style={styles.nextText}>
              {step === 2 ? '完成' : '下一步'}
            </Text>
          </TouchableOpacity>
        </View>

        {/* Content */}
        {renderStep()}

        {/* Footer Tips */}
        {step === 2 && (
          <Text style={styles.tipText}>
            💡 不用完美，记录真实就好
          </Text>
        )}
      </View>
    </Modal>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingTop: 60,
    paddingHorizontal: 20,
    paddingBottom: 20,
  },
  backButton: {
    padding: 8,
  },
  backText: {
    fontSize: 16,
    color: COLORS.textSecondary,
  },
  progressBar: {
    flex: 1,
    height: 4,
    backgroundColor: COLORS.border,
    borderRadius: 2,
    marginHorizontal: 16,
  },
  progressFill: {
    height: '100%',
    backgroundColor: COLORS.happy,
    borderRadius: 2,
  },
  nextButton: {
    padding: 8,
  },
  nextButtonDisabled: {
    opacity: 0.5,
  },
  nextText: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.text,
  },
  stepContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 40,
  },
  stepTitle: {
    fontSize: 28,
    fontWeight: '700',
    color: COLORS.text,
    marginBottom: 8,
    textAlign: 'center',
  },
  stepSubtitle: {
    fontSize: 16,
    color: COLORS.textSecondary,
    marginBottom: 40,
    textAlign: 'center',
  },
  emojiRow: {
    flexDirection: 'row',
    justifyContent: 'center',
    gap: 20,
  },
  emojiButton: {
    alignItems: 'center',
    padding: 16,
    borderRadius: 16,
    backgroundColor: COLORS.card,
    width: 80,
    shadowColor: COLORS.shadow,
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 1,
    shadowRadius: 8,
    elevation: 2,
  },
  emojiButtonSelected: {
    borderWidth: 2,
    borderColor: COLORS.happy,
  },
  emoji: {
    fontSize: 40,
    marginBottom: 8,
  },
  emojiLabel: {
    fontSize: 14,
    color: COLORS.textSecondary,
  },
  energyRow: {
    flexDirection: 'column',
    gap: 16,
    width: '100%',
  },
  energyButton: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 20,
    borderRadius: 16,
    backgroundColor: COLORS.card,
    justifyContent: 'center',
    gap: 16,
  },
  energyButtonSelected: {
    borderWidth: 2,
    borderColor: COLORS.happy,
  },
  energyEmoji: {
    fontSize: 24,
  },
  energyLabel: {
    fontSize: 16,
    fontWeight: '500',
    color: COLORS.text,
  },
  efficiencyRow: {
    flexDirection: 'row',
    justifyContent: 'center',
    gap: 16,
  },
  efficiencyButton: {
    alignItems: 'center',
    padding: 20,
    borderRadius: 16,
    backgroundColor: COLORS.card,
    width: 100,
  },
  efficiencyButtonSelected: {
    borderWidth: 2,
    borderColor: COLORS.happy,
  },
  efficiencyEmoji: {
    fontSize: 40,
    marginBottom: 8,
  },
  efficiencyLabel: {
    fontSize: 14,
    fontWeight: '500',
    color: COLORS.text,
  },
  tipText: {
    textAlign: 'center',
    fontSize: 14,
    color: COLORS.textSecondary,
    marginBottom: 40,
  },
});
