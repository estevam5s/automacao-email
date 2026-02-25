'use client';

import { useEffect, useState } from 'react';
import { useAppStore } from '@/lib/store';
import { formatCurrency } from '@/lib/utils';
import { Users, ClipboardList, Calendar, DollarSign, CheckCircle, Clock, TrendingUp } from 'lucide-react';

export default function DashboardPage() {
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
        setRanking(rankingData.slice(0, 5));
        
        await salvarLog({
          acao: 'VISUALIZAR',
          tabela: 'dashboard',
          registro_id: 'dashboard',
          usuario: 'sistema',
        });
      } catch (error) {
        console.error('Erro ao carregar dados:', error);
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, [getTotalFuncionarios, getRankingPagamentos, salvarLog]);

  const statCards = [
    { label: 'Funcionários', value: stats.total_cadastrados, icon: Users, color: 'from-cyan-500 to-blue-500' },
    { label: 'Registros', value: stats.total_registros, icon: ClipboardList, color: 'from-purple-500 to-pink-500' },
    { label: 'Dias Trab.', value: stats.total_dias_trabalhados, icon: Calendar, color: 'from-amber-500 to-orange-500' },
    { label: 'Total Geral', value: formatCurrency(stats.total_geral_pago), icon: DollarSign, color: 'from-green-500 to-emerald-500', isCurrency: true },
    { label: 'Total Pago', value: formatCurrency(stats.total_pago), icon: CheckCircle, color: 'from-blue-500 to-cyan-500', isCurrency: true },
    { label: 'Pendente', value: formatCurrency(stats.total_pendente), icon: Clock, color: 'from-red-500 to-pink-500', isCurrency: true },
  ];

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-cyan-400" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Dashboard</h1>
        <p className="text-slate-400">Visão geral do sistema de salários</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {statCards.map((stat, index) => (
          <div
            key={index}
            className="bg-slate-800 rounded-xl p-6 border border-slate-700 hover:border-slate-600 transition-all"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-slate-400 text-sm">{stat.label}</p>
                <p className="text-2xl font-bold text-white mt-1">{stat.value}</p>
              </div>
              <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${stat.color} flex items-center justify-center`}>
                <stat.icon className="h-6 w-6 text-white" />
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="bg-slate-800 rounded-xl border border-slate-700">
        <div className="p-6 border-b border-slate-700">
          <div className="flex items-center gap-2">
            <TrendingUp className="h-5 w-5 text-cyan-400" />
            <h2 className="text-lg font-semibold text-white">Top 5 - Ranking de Pagamentos</h2>
          </div>
        </div>
        <div className="p-6">
          {ranking.length > 0 ? (
            <div className="space-y-4">
              {ranking.map((item, index) => (
                <div
                  key={index}
                  className="flex items-center justify-between p-4 bg-slate-700/50 rounded-lg"
                >
                  <div className="flex items-center gap-4">
                    <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm ${
                      index === 0 ? 'bg-yellow-500/20 text-yellow-400' :
                      index === 1 ? 'bg-slate-400/20 text-slate-300' :
                      index === 2 ? 'bg-amber-600/20 text-amber-500' :
                      'bg-slate-600/20 text-slate-400'
                    }`}>
                      #{item.posicao}
                    </div>
                    <div>
                      <p className="font-medium text-white">{item.nome}</p>
                      <p className="text-sm text-slate-400">{item.dias_trabalhados} dias trabalhados</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="font-semibold text-cyan-400">{formatCurrency(item.total_recebido)}</p>
                    <p className="text-sm text-slate-400">Média: {formatCurrency(item.media_diaria)}/dia</p>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-slate-400 text-center py-8">Nenhum registro encontrado</p>
          )}
        </div>
      </div>
    </div>
  );
}
