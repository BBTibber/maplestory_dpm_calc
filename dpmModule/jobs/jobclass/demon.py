from ...kernel import core
from ...kernel.core import VSkillModifier as V
from ...kernel.core import CharacterModifier as MDF
from ...character import characterKernel as ck
from functools import partial

'''
최대 HP의 20% 소비, 55초[(스킬 레벨+30)초] 동안 마스테마 소환, 재사용 대기시간 150초, 소환된 마스테마는 스스로의 판단으로 아래의 스킬을 시전
마스테마 클로우: 최대 8명의 적을 1000%[(스킬 레벨*20+500)%의 데미지]의 데미지로 8번 공격, 재사용 대기시간 5초
러블리 테리토리: 6초 동안 최대 HP의 일정 비율로 피해를 입히는 공격을 포함한 피격 데미지 22%를 2회 감소시키는 버프를 시전, 지속시간이 끝나거나 감소 횟수를 모두 소비하면 버프 소멸, 재사용 대기시간 8초

'''

class AnotherWorldGoddessWrapper(core.BuffSkillWrapper):
    def __init__(self, vEhc, num1, num2):
        self.vlevel = vEhc.getV(num1, num2)
        vlevel = self.vlevel
        super(AnotherWorldGoddessWrapper, self).__init__(skill = core.BuffSkill("이계 여신의 축복", num1, num2, pdamage_indep=6+(vlevel-1)//5).isV(vEhc, num1, num2))
        self.skillList = [core.BuffSkill("회복의 축복"), core.BuffSkill("방패의 축복"), core.BuffSkill("보호의 축복"), core.BuffSkill(("이계의 공허"))]

'''
최대 HP의 5% 소비, 40초 동안 최종 데미지 [1레벨에서 6%, 6, 11, 16, 21, 26레벨에서 1%씩 증가] 증가, 일정 시간마다 각종 축복 및 공격을 시전, 축복 시전 시 이전 축복이 남아있다면 소멸
회복의 축복: DF/PP/HP 중 자신이 사용하는 쪽을 최대치의 27%[(15 + 스킬레벨/2)%, 소수점은 버린다.] 회복, 특정한 회복 불가 상황에도 회복 가능
방패의 축복: 1회에 한해 최대 HP의 일정 비율로 피해를 입히는 공격을 포함한 피격 데미지 70%[(45 + 스킬레벨)%] 감소
보호의 축복: 1회에 한해 치명적인 상태이상 방어
이계의 공허: 최대 12명의 적을 2400%[(1200 + 48*스킬레벨)%의 데미지]의 데미지로 12번 공격
재사용 대기시간 120초
'''