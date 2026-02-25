'use client';

import { useEffect, useState } from 'react';
import { useAppStore } from '@/lib/store';
import { formatCurrency } from '@/lib/utils';
import { Loader2, Trophy } from 'lucide-react';

export default function EstatisticasPage() {
  const { getTotalFuncionarios, getRankingPagamentos, salvarLog } = useAppStore();
  const [stats, setStats] = useState({
    total_cadastrados: 0,
    total_registros: 0,
    total_dias_trabalhados: 0,
    total_geral_pago: 0,
    total_pago: 0,
    total_pendente: 0,
  });
  const [ranking, setRanking] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      try {
        const [statsData, rankingData] = await Promise.all([
          getTotalFuncionarios(),
          getRankingPagamentos()
        ]);
        setStats(statsData);
        setRanking(rankingData);
        
        await salvarLog({ acao: 'VISUALIZAR', tabela: 'estatisticas', registro_id: 'estatisticas', usuario: 'sistema' });
      } catch (error) {
        console.error('Erro ao carregar dados:', error);
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="h-8 w-8 animate-spin text-cyan-400" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Estatísticas</h1>
        <p className="text-slate-400">Dados consolidados do sistema</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-gradient-to-br from-cyan-500 to-blue-600 rounded-xl p-6 text-white">
          <p className="text-cyan-100">Total Geral</p>
          <p className="text-3xl font-bold mt-2">{formatCurrency(stats.total_geral_pago)}</p>
          <p className="text-cyan-100 text-sm mt-2">{stats.total_registros} registros</p>
        </div>
        <div className="bg-gradient-to-br from-green-500 to-emerald-600 rounded-xl p-6 text-white">
          <p className="text-green-100">Total Pago</p>
          <p className="text-3xl font-bold mt-2">{formatCurrency(stats.total_pago)}</p>
          <p className="text-green-100 text-sm mt-2">{stats.total_cadastrados} funcionários</p>
        </div>
        <div className="bg-gradient-to-br from-yellow-500 to-orange-600 rounded-xl p-6 text-white">
          <p className="text-yellow-100">Total Pendente</p>
          <p className="text-3xl font-bold mt-2">{formatCurrency(stats.total_pendente)}</p>
          <p className="text-yellow-100 text-sm mt-2">{stats.total_dias_trabalhados} dias</p>
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-slate-800 rounded-xl p-6 border border-slate-700">
          <p className="text-slate-400 text-sm">Funcionários</p>
          <p className="text-2xl font-bold text-white mt-1">{stats.total_cadastrados}</p>
        </div>
        <div className="bg-slate-800 rounded-xl p-6 border border-slate-700">
          <p className="text-slate-400 text-sm">Registros</p>
          <p className="text-2xl font-bold text-white mt-1">{stats.total_registros}</p>
        </div>
        <div className="bg-slate-800 rounded-xl p-6 border border-slate-700">
          <p className="text-slate-400 text-sm">Dias Trab.</p>
          <p className="text-2xl font-bold text-white mt-1">{stats.total_dias_trabalhados}</p>
        </div>
        <div className="bg-slate-800 rounded-xl p-6 border border-slate-700">
          <p className="text-slate-400 text-sm">Média/Dia</p>
          <p className="text-2xl font-bold text-cyan-400 mt-1">
            {stats.total_dias_trabalhados > 0 ? formatCurrency(stats.total_geral_pago / stats.total_dias_trabalhados) : formatCurrency(0)}
          </p>
        </div>
      </div>

      <div className="bg-slate-800 rounded-xl border border-slate-700">
        <div className="p-6 border-b border-slate-700 flex items-center gap-2">
          <Trophy className="h-5 w-5 text-yellow-400" />
          <h2 className="text-lg font-semibold text-white">Ranking de Pagamentos</h2>
        </div>
        <div className="p-6">
          {ranking.length > 0 ? (
            <div className="space-y-3">
              {ranking.map((item, index) => (
                <div
                  key={index}
                  className="flex items-center justify-between p-4 bg-slate-700/50 rounded-lg"
                >
                  <div className="flex items-center gap-4">
                    <div className={`w-10 h-10 rounded-full flex items-center justify-center font-bold ${
                      index === 0 ? 'bg-yellow-500/20 text-yellow-400' :
                      index === 1 ? 'bg-slate-400/20 text-slate-300' :
                      index === 2 ? 'bg-amber-600/20 text-amber-500' :
                      'bg-slate-600/20 text-slate-400'
                    }`}>
                      {index === 0 ? '🥇' : index === 1 ? '🥈' : index === 2 ? '🥉' : `#${item.posicao}`}
                    </div>
                    <div>
                      <p className="font-medium text-white">{item.nome}</p>
                      <p className="text-sm text-slate-400">{item.dias_trabalhados} dias • Média: {formatCurrency(item.media_diaria)}/dia</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="font-semibold text-cyan-400 text-lg">{formatCurrency(item.total_recebido)}</p>
                    <p className="text-sm text-slate-400">
                      <span className="text-green-400">{formatCurrency(item.total_pago)}</span> / 
                      <span className="text-yellow-400"> {formatCurrency(item.total_pendente)}</span>
                    </p>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-slate-400 text-center py-8">Nenhum dado disponível</p>
          )}
        </div>
      </div>
    </div>
  );
}
