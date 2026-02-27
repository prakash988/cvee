# THIS is what makes CogniMem feel different from every database on Earth

import asyncio

class LivingCogniMem:
    """CogniMem that's always thinking, even when nobody's asking."""
    
    async def breathe(self):
        """The heartbeat. Runs forever."""
        while self._alive:
            # Sentinel: "Anything contradictory since last check?"
            contradictions = await self.sentinel.scan()
            for c in contradictions:
                self.communicate(CogniMessage(
                    type=MessageType.CONTRADICTION,
                    priority=MessagePriority.HIGH,
                    content=f"Found contradiction: {c.description}",
                    data=c
                ))
            
            # Connector: "Any new cross-domain links?"
            connections = await self.connector.discover()
            for conn in connections:
                self.communicate(CogniMessage(
                    type=MessageType.INSIGHT,
                    priority=MessagePriority.MEDIUM,
                    content=f"Discovered connection: {conn.description}",
                    data=conn
                ))
            
            # Gardener: "Anything needs pruning or strengthening?"
            await self.gardener.tend()
            
            # Prophet: "What will they need next?"
            predictions = await self.prophet.anticipate()
            for p in predictions:
                await self.prefetch(p)
            
            # Skeptic: "Am I still calibrated? Any overconfidence?"
            await self.skeptic.self_check()
            
            # Librarian: "Should I re-index anything?"
            await self.librarian.optimize()
            
            await asyncio.sleep(self.heartbeat_interval)
    
    def start(self):
        """CogniMem wakes up."""
        self._alive = True
        asyncio.create_task(self.breathe())
        # CogniMem is now ALIVE and THINKING