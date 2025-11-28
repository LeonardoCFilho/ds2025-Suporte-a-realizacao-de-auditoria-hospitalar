"""
Base de Conhecimento Médico Completa para o Sistema LLM
Contém protocolos, regras e critérios médicos para TODAS as patologias
"""
import json
from typing import Dict, Any, List
from .data_knowledge_base import data_protocols, data_discharge_criteria, data_load_player_rules

class MedicalKnowledgeBase:
    """Base de conhecimento médico especializada em critérios de alta"""
    
    def __init__(self):
        self.protocols = self._load_medical_protocols()
        self.discharge_criteria = self._load_discharge_criteria()
        self.payer_rules = self._load_payer_rules()
    
    def _load_medical_protocols(self) -> Dict[str, Any]:
        """Carrega protocolos médicos baseados em evidências - VERSÃO COMPLETA"""
        return data_protocols
    
    def _load_discharge_criteria(self) -> Dict[str, Any]:
        """Critérios gerais de segurança para alta hospitalar"""
        return data_discharge_criteria
    
    def _load_payer_rules(self) -> Dict[str, Any]:
        """Regras de pagadores (operadoras de saúde) - VERSÃO COMPLETA"""
        return data_load_player_rules
    
    def get_protocol(self, pathology: str) -> Dict[str, Any]:
        """Obtém protocolo específico para uma patologia"""
        return self.protocols.get(pathology, {})
    
    def check_payer_compliance(self, pathology: str, current_stay: int) -> Dict[str, Any]:
        """Verifica conformidade com regras do pagador"""
        max_stay = self.payer_rules['max_length_of_stay'].get(pathology, self.payer_rules['max_length_of_stay']['DEFAULT'])
        
        return {
            'max_allowed_stay': max_stay,
            'current_stay': current_stay,
            'excess_days': max(0, current_stay - max_stay),
            'is_compliant': current_stay <= max_stay,
            'alert_triggered': current_stay > max_stay,
            'compliance_level': 'COMPLIANT' if current_stay <= max_stay else 'NON_COMPLIANT'
        }
    
    def assess_discharge_readiness(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Avalia prontidão para alta baseada em múltiplos critérios"""
        pathology = patient_data.get('patologia', '')
        current_stay = patient_data.get('tempo_permanencia', 0)
        age = patient_data.get('idade', 0)
        comorbidities = patient_data.get('comorbidades', [])
        
        protocol = self.get_protocol(pathology)
        payer_status = self.check_payer_compliance(pathology, current_stay)
        
        # Calcular score de prontidão
        readiness_score = 0
        factors = []
        
        # Fator tempo de internação vs protocolo
        avg_stay = protocol.get('avg_length_of_stay', 5)
        if current_stay >= avg_stay:
            readiness_score += 25
            factors.append(f'Tempo de internação adequado ({current_stay}/{avg_stay} dias)')
        
        # Fator conformidade pagador
        if payer_status['is_compliant']:
            readiness_score += 25
            factors.append('Dentro dos limites do pagador')
        
        # Fator idade (penaliza idosos)
        if age < 65:
            readiness_score += 20
            factors.append('Idade <65 anos - menor risco')
        elif age > 80:
            readiness_score -= 10
            factors.append('Idade >80 anos - maior risco')
        
        # Fator comorbidades
        if not comorbidities or comorbidities == ['NENHUMA']:
            readiness_score += 20
            factors.append('Sem comorbidades significativas')
        elif len(comorbidities) >= 3:
            readiness_score -= 15
            factors.append('Múltiplas comorbidades - maior risco')
        
        # Fator setor
        setor = patient_data.get('setor', '')
        if setor != 'UTI':
            readiness_score += 10
            factors.append('Paciente fora da UTI')
        
        # Normalizar score
        readiness_score = max(0, min(100, readiness_score))
        
        return {
            'readiness_score': readiness_score,
            'readiness_level': self._get_readiness_level(readiness_score),
            'factors': factors,
            'protocol_reference': protocol,
            'payer_status': payer_status,
            'recommendation': self._generate_recommendation(readiness_score, pathology)
        }
    
    def _get_readiness_level(self, score: int) -> str:
        """Converte score em nível de prontidão"""
        if score >= 80:
            return 'ALTA_PRIORIDADE_ALTA'
        elif score >= 60:
            return 'ALTA_PRIORIDADE_MEDIA'
        elif score >= 40:
            return 'ALTA_PRIORIDADE_BAIXA'
        else:
            return 'MANTER_INTERNACAO'
    
    def _generate_recommendation(self, score: int, pathology: str) -> str:
        """Gera recomendação baseada no score"""
        if score >= 80:
            return f"Paciente com {pathology} apresenta alta probabilidade de alta segura. Recomendação: Alta Prioridade Alta."
        elif score >= 60:
            return f"Paciente com {pathology} pode ser considerado para alta. Recomendação: Avaliação clínica para confirmação."
        elif score >= 40:
            return f"Paciente com {pathology} necessita de mais avaliação. Recomendação: Revisar em 24-48h."
        else:
            return f"Paciente com {pathology} deve manter internação. Recomendação: Continuar tratamento."

# Instância global para uso
medical_kb = MedicalKnowledgeBase()