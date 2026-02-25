'use client';

import { useEffect, useState } from 'react';
import { useAppStore } from '@/lib/store';
import { Loader2 } from 'lucide-react';

export default function ConfigPage() {
  const { getConfiguracao, salvarConfiguracao, salvarLog } = useAppStore();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [emailDestinatario, setEmailDestinatario] = useState('');
  const [emailRemetente, setEmailRemetente] = useState('');
  const [senhaApp, setSenhaApp] = useState('');
  const [smtpHost, setSmtpHost] = useState('smtp.gmail.com');
  const [smtpPort, setSmtpPort] = useState('587');

  useEffect(() => {
    const loadConfig = async () => {
      try {
        const config = await getConfiguracao();
        if (config) {
          setEmailDestinatario(config.email_destinatario || '');
          setEmailRemetente(config.email_remetente || '');
          setSenhaApp(config.senha_app || '');
          setSmtpHost(config.smtp_host || 'smtp.gmail.com');
          setSmtpPort(String(config.smtp_port || 587));
        }
      } catch (error) {
        console.error('Erro ao carregar configurações:', error);
      } finally {
        setLoading(false);
      }
    };
    loadConfig();
  }, []);

  const handleSalvar = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try {
      await salvarConfiguracao({
        email_destinatario: emailDestinatario,
        email_remetente: emailRemetente,
        senha_app: senhaApp,
        smtp_host: smtpHost,
        smtp_port: parseInt(smtpPort),
      });
      await salvarLog({ acao: 'ATUALIZAR', tabela: 'configuracoes', registro_id: 'config-email', usuario: 'sistema' });
      alert('Configurações salvas com sucesso!');
    } catch (error) {
      console.error('Erro ao salvar:', error);
      alert('Erro ao salvar configurações');
    } finally {
      setSaving(false);
    }
  };

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
        <h1 className="text-2xl font-bold text-white">Configurações</h1>
        <p className="text-slate-400">Configure as opções do sistema</p>
      </div>

      <div className="max-w-2xl">
        <div className="bg-slate-800 rounded-xl border border-slate-700 p-6">
          <h2 className="text-lg font-semibold text-white mb-6">Configurações de E-mail</h2>
          
          <form onSubmit={handleSalvar} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-1">E-mail Remetente</label>
              <input
                type="email"
                value={emailRemetente}
                onChange={(e) => setEmailRemetente(e.target.value)}
                className="w-full px-4 py-2 bg-slate-900 border border-slate-600 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-500"
                placeholder="seu@email.com"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-300 mb-1">E-mail Destinatário</label>
              <input
                type="email"
                value={emailDestinatario}
                onChange={(e) => setEmailDestinatario(e.target.value)}
                className="w-full px-4 py-2 bg-slate-900 border border-slate-600 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-500"
                placeholder="destinatario@email.com"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-300 mb-1">Senha de App Gmail</label>
              <input
                type="password"
                value={senhaApp}
                onChange={(e) => setSenhaApp(e.target.value)}
                className="w-full px-4 py-2 bg-slate-900 border border-slate-600 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-500"
                placeholder="Senha de 16 caracteres"
                required
              />
              <p className="text-xs text-slate-500 mt-1">
                Para obter a senha de app do Gmail: myaccount.google.com/apppasswords
              </p>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-1">Servidor SMTP</label>
                <input
                  type="text"
                  value={smtpHost}
                  onChange={(e) => setSmtpHost(e.target.value)}
                  className="w-full px-4 py-2 bg-slate-900 border border-slate-600 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-500"
                  placeholder="smtp.gmail.com"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-1">Porta SMTP</label>
                <input
                  type="number"
                  value={smtpPort}
                  onChange={(e) => setSmtpPort(e.target.value)}
                  className="w-full px-4 py-2 bg-slate-900 border border-slate-600 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-500"
                  placeholder="587"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={saving}
              className="flex items-center justify-center gap-2 w-full px-4 py-3 bg-cyan-500 hover:bg-cyan-600 text-white rounded-lg font-medium transition-colors disabled:opacity-50"
            >
              {saving ? <Loader2 className="h-5 w-5 animate-spin" /> : null}
              {saving ? 'Salvando...' : 'Salvar Configurações'}
            </button>
          </form>
        </div>

        <div className="bg-slate-800 rounded-xl border border-slate-700 p-6 mt-6">
          <h2 className="text-lg font-semibold text-white mb-4">Informações do Banco de Dados</h2>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-slate-400">URL:</span>
              <span className="text-white font-mono text-sm">https://igmnzakdeacfddjeduoc.supabase.co</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Status:</span>
              <span className="text-green-400">🟢 Conectado</span>
            </div>
          </div>
        </div>

        <div className="bg-slate-800 rounded-xl border border-slate-700 p-6 mt-6">
          <h2 className="text-lg font-semibold text-white mb-4">Tabelas do Banco</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {[
              { name: 'funcionarios', desc: 'Registros de salários' },
              { name: 'funcionarios_base', desc: 'Lista de funcionários' },
              { name: 'configuracoes', desc: 'Configurações de e-mail' },
              { name: 'observacoes_gerais', desc: 'Observações diárias' },
              { name: 'registros_trabalho', desc: 'Controle de dias' },
              { name: 'logs', desc: 'Histórico de ações' },
            ].map((table) => (
              <div key={table.name} className="bg-slate-700/50 rounded-lg p-3">
                <p className="font-medium text-white">{table.name}</p>
                <p className="text-sm text-slate-400">{table.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
