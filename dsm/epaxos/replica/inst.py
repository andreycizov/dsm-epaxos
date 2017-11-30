from dsm.epaxos.inst.store import InstanceStore
from dsm.epaxos.net.packet import Packet
from dsm.epaxos.replica.acceptor.main import AcceptorCoroutine
from dsm.epaxos.replica.client.main import ClientsActor
from dsm.epaxos.replica.config import ReplicaState
from dsm.epaxos.replica.leader.main import LeaderCoroutine
from dsm.epaxos.replica.main.ev import Tick, Wait
from dsm.epaxos.replica.main.main import MainCoroutine
from dsm.epaxos.replica.net.main import NetActor
from dsm.epaxos.replica.quorum.ev import Configuration, Quorum
from dsm.epaxos.replica.state.main import StateActor


class Replica:
    def __init__(self, quorum: Quorum, config: Configuration, net_actor: NetActor):
        self.quorum = quorum
        self.store = InstanceStore()

        state = StateActor().run()
        clients = ClientsActor().run()
        leader = LeaderCoroutine(quorum, ).run()
        acceptor = AcceptorCoroutine(quorum, config).run()
        net = net_actor.run()

        next(state)
        next(clients)
        next(leader)
        next(acceptor)
        next(net)

        self.main = MainCoroutine(
            state,
            clients,
            leader,
            acceptor,
            net
        ).run()

        assert isinstance(next(self.main), Wait)

    def packet(self, p: Packet):
        self.main.send(p)

    def tick(self, idx):
        self.main.send(Tick(idx))
