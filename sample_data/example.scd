<?xml version="1.0" encoding="UTF-8"?>
<SCL xmlns="http://www.iec.ch/61850/2003/SCL" version="2007" revision="B">

  <Header id="ExampleSubstation" version="1.0" toolID="scd-ids-rulegen-sample"/>

  <!-- IEDs: the physical/logical devices deployed in the substation -->
  

  <IED name="ProtRelay1" type="REF615" manufacturer="ExampleVendor" desc="Feeder protection relay, Bay 1">
    <AccessPoint name="P1">
      <Server>
        <LDevice inst="PROT">
          <LN0 lnClass="LLN0" inst="" lnType="LLN0_Prot">
            <DOI name="Mod"/>
            <DataSet name="GooseDataSet1">
              <FCDA ldInst="PROT" lnClass="PTOC" doName="Op" fc="ST"/>
            </DataSet>
            <GSEControl name="gcbTrip" datSet="GooseDataSet1" appID="1001" confRev="1"/>
          </LN0>
          <LN lnClass="PTOC" inst="1" lnType="PTOC_Basic" desc="Overcurrent protection"/>
        </LDevice>
      </Server>
    </AccessPoint>
  </IED>

  <IED name="ProtRelay2" type="REF615" manufacturer="ExampleVendor" desc="Feeder protection relay, Bay 2">
    <AccessPoint name="P1">
      <Server>
        <LDevice inst="PROT">
          <LN0 lnClass="LLN0" inst="" lnType="LLN0_Prot">
            <DOI name="Mod"/>
            <DataSet name="GooseDataSet2">
              <FCDA ldInst="PROT" lnClass="PTOC" doName="Op" fc="ST"/>
            </DataSet>
            <GSEControl name="gcbTrip" datSet="GooseDataSet2" appID="1002" confRev="1"/>
          </LN0>
          <LN lnClass="PTOC" inst="1" lnType="PTOC_Basic" desc="Overcurrent protection"/>
        </LDevice>
      </Server>
    </AccessPoint>
  </IED>

  <IED name="BayController1" type="REC615" manufacturer="ExampleVendor" desc="Bay controller / gateway, Bay 1">
    <AccessPoint name="P1">
      <Server>
        <LDevice inst="CTRL">
          <LN0 lnClass="LLN0" inst="" lnType="LLN0_Ctrl">
            <DOI name="Mod"/>
          </LN0>
          <LN lnClass="XCBR" inst="1" lnType="XCBR_Basic" desc="Circuit breaker control"/>
        </LDevice>
      </Server>
    </AccessPoint>
  </IED>

  <IED name="StationHMI" type="SYS600" manufacturer="ExampleVendor" desc="Station-level HMI / MMS client">
    <AccessPoint name="P1">
      <Server>
        <LDevice inst="HMI">
          <LN0 lnClass="LLN0" inst="" lnType="LLN0_HMI">
            <DOI name="Mod"/>
          </LN0>
        </LDevice>
      </Server>
    </AccessPoint>
  </IED>

  
  <!-- Communication section: maps each IED's AccessPoint to a real -->
  <!-- network address (IP/MAC) and a subnetwork.                   -->
  

  <Communication>
    <SubNetwork name="StationBus" type="8-MMS">
      <ConnectedAP iedName="ProtRelay1" apName="P1">
        <Address>
          <P type="IP">192.168.10.11</P>
          <P type="IP-SUBNET">255.255.255.0</P>
          <P type="OSI-AP-Title">1,3,9999,23</P>
          <P type="MAC-Address">00:0C:CD:01:00:11</P>
        </Address>
        <GSE ldInst="PROT" cbName="gcbTrip">
          <Address>
            <P type="MAC-Address">01:0C:CD:01:00:01</P>
            <P type="APPID">1001</P>
            <P type="VLAN-ID">100</P>
          </Address>
        </GSE>
      </ConnectedAP>

      <ConnectedAP iedName="ProtRelay2" apName="P1">
        <Address>
          <P type="IP">192.168.10.12</P>
          <P type="IP-SUBNET">255.255.255.0</P>
          <P type="OSI-AP-Title">1,3,9999,24</P>
          <P type="MAC-Address">00:0C:CD:01:00:12</P>
        </Address>
        <GSE ldInst="PROT" cbName="gcbTrip">
          <Address>
            <P type="MAC-Address">01:0C:CD:01:00:02</P>
            <P type="APPID">1002</P>
            <P type="VLAN-ID">100</P>
          </Address>
        </GSE>
      </ConnectedAP>

      <ConnectedAP iedName="BayController1" apName="P1">
        <Address>
          <P type="IP">192.168.10.21</P>
          <P type="IP-SUBNET">255.255.255.0</P>
          <P type="OSI-AP-Title">1,3,9999,31</P>
          <P type="MAC-Address">00:0C:CD:01:00:21</P>
        </Address>
      </ConnectedAP>

      <ConnectedAP iedName="StationHMI" apName="P1">
        <Address>
          <P type="IP">192.168.10.51</P>
          <P type="IP-SUBNET">255.255.255.0</P>
          <P type="OSI-AP-Title">1,3,9999,51</P>
          <P type="MAC-Address">00:0C:CD:01:00:51</P>
        </Address>
      </ConnectedAP>
    </SubNetwork>
  </Communication>

</SCL>
